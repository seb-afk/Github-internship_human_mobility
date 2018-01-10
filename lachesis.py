import pandas as pd
from datetime import timedelta
from sklearn.metrics.pairwise import euclidean_distances, pairwise_distances
import numpy as np
from scipy.spatial.distance import pdist, cdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster
from joblib import delayed, Parallel
from IPython.display import clear_output


def meters2degrees(meters):
    """
    Converts meters to degrees.

    Parameters:
    meters -- input in meters

    Returns:
    degrees -- output in degrees
    """
    degrees = meters * (1 / 111319.9)
    return degrees


def degrees2meters(degrees):
    """
    Converts degrees to meters.

    Parameters:
    degrees -- input in degrees

    Returns:
    meters -- output in meters
    """
    return degrees * 111319.9


def get_stop_location(df, min_stay_duration, roaming_distance, 
is_sorted=False):
    """
    Extract the stop-locations and return them as a Pandas dataframe.
    Source: "Hariharan, Toyama. 2004. Project Lachesis: Parsing and 
    Modeling Location Histories"

    Parameters:
    df -- Numpy array [[timestamp, longitude, latitude]] of size (N x 3)
    min_stay_duration -- Minimum stay duration in minutes
    roaming_distance -- Maximum roaming distance in meters
    is_sorted -- Boolean Flag indicating if df is time-ordered.

    Returns:
    -- Pandas df [[timestamp, latitude, longitude, t_start, t_end]]
    """
    # Sort array by timestamp if is_sorted flag has not been set
    if not is_sorted:
        df = df[df[:, 0].argsort()]
    # Initialise variables
    i = 0
    medoids_set = set()

    while i < df.shape[0]:
        # Get the first item that is at least min_stay_duration away from
        # point i
        time_cutoff = df[i, 0] + timedelta(minutes=min_stay_duration)
        idxs_after_time_cutoff = np.where(df[:, 0] >= time_cutoff)
        # Break out of while loop if there are no more items that 
        # satisfy the time_cutoff criterium
        if len(idxs_after_time_cutoff[0]) == 0:
            break

        # This is the first item after that satisfies time_cutoff
        j_star = idxs_after_time_cutoff[0][0]

        # Check if roaming_distance criterium is satisfied. If point
        # exceed roaming distance them move on. Otherwise incrementally
        # expand set of points to be included until roaming distance is
        # exceeded (or no more datapoints are left)
        if np.max(pdist(df[i:j_star + 1, [1, 2]])) > roaming_distance:
            i += 1
        else:
            j_star = i + 1
            # Expand sets of points by incrementally checking subsequent
            # points in time and checking whether they are within the 
            # roaming distance.
            while j_star < df.shape[0]:
                max_distance = np.max(cdist(df[i:j_star + 1, [1, 2]], 
                df[j_star, [1, 2]].reshape(1, -1)))
                if max_distance <= roaming_distance:
                    j_star += 1
                else:
                    break
            j_star -= 1

            # Get medoid, if there are only 2 points just take the first
            if (j_star - i) == 1:
                medoid_idx = 0
            else:
                # Compute full distance matrix of this current set of
                # points,convert to squareform and get the medoid of all
                # these points
                medoid_idx = np.argmin(
                    np.sum(squareform(pdist(df[i:j_star + 1, [1, 2]])),
                    axis=0))

            # Add medoid to list and increment i-index
            medoids_set.add(tuple(list(df[i + medoid_idx]) +
                                  [df[i, 0], df[j_star, 0]]))
            i = j_star + 1

    # Convert to dataframe and return as result
    df_result = pd.DataFrame(list(medoids_set),
                             columns=["timestamp", "latitude", "longitude",
                                      "t_start", "t_end"])
    return df_result


def get_medoid_index(X):
    """
    Returns the index of the medoid of the points in X. 
    Note: The medoid is the point closest to all the other points in 
    the set.

    Parameters:
    X -- Numpy vector [[longitude, latitude]]

    Returns:
    Index of the medoid of X.
    """
    dist_mat = pairwise_distances(X)
    return np.argmin(np.sum(dist_mat, axis=0))


def get_clustermedoids_indeces(X):
    """
    Return the index of the medoid of each cluster in X.

    Parameters:
    X -- Numpy array [[cluster_assignment, longitude, latitude]]

    Returns:
    A list of indeces pointing to the medoid for each cluster in X.
    """
    X = X.values
    medoid_idx_list = []
    for cluster_i in np.unique(X[:, 0]):
        current_cluster_idx = np.where(X[:, 0] == cluster_i)[0]
        medoid_idx_list.append(
        current_cluster_idx[get_medoid_index(X[current_cluster_idx, 1:])])
    return medoid_idx_list


def calculate_centroid(X):
    """
    Calculates the centroid of an array of longitude-latitude pairs.

    Parameters:
    X -- Numpy array [[longitude, latitude]]

    Returns:
    Centroid of X
    """
    return np.mean(X, axis=0)


def rgiration_at_k(X, k=None, ignore_weigths=False):
    """
    Calculates the radius of gyration at k.

    Parameters:
    ignore_weigths -- True if the visitation count at a destination 
    should not be used as weight in final R-gyration calculation.
    X --  A pandas dataframe with columns [[longitude, latitude, count]]
    :param k -- How many of the most visited destinations to consider.

    Returns:
    Integer representing the radius of giraiton @k. If k is not
    specified it returns the total radius of giration. If the number of
    destinations in X is smaller than k np.NaN is returned.
    """

    # Check that k is admissibile
    if k == None:
        k = X.shape[0]
    elif (k == 0) or (k > X.shape[0]):
        return np.nan

    # Convert to numpy array and sort
    X = X.values
    X = X[X[:, 2].argsort()][::-1]  
    X = X[:k]

    # In case the ignore weights parameter is set.
    if ignore_weigths:
        X[:, 2] = 1

    counts = X[:, 2]
    difference_squared = euclidean_distances(X[:, :2], calculate_centroid(X[:, :2])\
        .reshape(1, -1), squared=True)
    return float(degrees2meters((np.dot(counts.T, difference_squared) / sum(counts))**0.5))


def process_user(df_current, i, current_user, n_users, min_stay, roam_dist, print_output=None):
    """
    Helper function to extract the stop locations of one user out of many users. 
    Note: Required to parallel process data in process_data function.

    Parameters:
    df_current -- Pandas dataframe [[user_id, timestamp, latitude, longitude]].
                  Note: Columns "user_id" and "timestamp" are set as the index
    i -- Incremental counter
    current_user -- user_id of user being processed
    n_users -- Total number of users
    min_stay -- Minimum stay duration in minutes
    roam_dist -- Maximum roaming distance in meters
    print_output -- String to indicate whether to print output. ["yes", "notebook"]

    Returns:
    df_user_stops -- Pandas dataframe of stop locations structured like
                     [[timestamp, latitude, longitude, t_start, t_end]]
    """
    # Print progress only occasionally.
    if ((i+1) % (n_users//50)) == 0:
        if print_output == "yes":
            print("Processing user {} of {}.".format(i + 1, n_users))
        elif print_output == "notebook":
            clear_output(wait=True)
            print("Processing user {} of {}.".format(i + 1, n_users))

    df_user_stops = get_stop_location(
        df_current, min_stay_duration=min_stay, roaming_distance=roam_dist)
    df_user_stops["user_id"] = current_user
    return df_user_stops


def process_data(df, roam_dist, min_stay, n_jobs=1, print_output=None):
    """
    Process entire dataset to extract stop locations.
    Note: for parallel processing set n_jobs > 1.

    Parameters:
    df -- Pandas dataframe [[user_id, timestamp, latitude, longitude]].
                  Note: Columns "user_id" and "timestamp" are set as the index
    n_users -- Total number of users
    min_stay -- Minimum stay duration in minutes
    roam_dist -- Maximum roaming distance in meters
    print_output -- String to indicate whether to print output. 
                    ["yes" "notebook"]

    Returns:
    df_user_stops -- Pandas dataframe of stop locations structured like
                     [[timestamp, latitude, longitude, t_start, t_end]]
    """
    userids = list(df.index.levels[0])
    n_users = len(userids)
    # Get stops for each user
    df_stops = Parallel(n_jobs=n_jobs)\
        (delayed(process_user)\
        (np.array(df.loc[userids[i], ["latitude", "longitude"]].reset_index()),
         i, userids[i], n_users, min_stay, roam_dist, print_output) 
         for i in range(n_users))
    return df_stops


def cluster_stoplocations(df, method, max_d):
    """
    Takes df with lon-lat coordinates and assigns each observation to a
    cluster based on the clustering method and max distance choosen.

    Parameters:
    df -- Pandas dataframe. Must contain columns ["longitude","latitude"]
    method -- clustering method. See SciPy docs for linkage methods
    max_d -- spatial distance threshold to use. See SciPy docs

    Returns:
    df -- Pandas dataframe same as input but with added
          cluster_assignment column.
    """
    Z = linkage(df.loc[:, ["longitude", "latitude"]],
                method=method, metric="euclidean")
    df.loc[:, "cluster_assignment"] = fcluster(Z, max_d, criterion='distance')
    return df


def get_clustermedoids(df):
    """
    Gets the medoids for each cluster in a dataframe.

    Parameters:
    df -- Pandas dataframe consisting of lon-lat coordinates and cluster
          assignments for each observation.

    Returns:
    df -- Pandas dataframe containing the medoid of each cluster
    """
    medoids_idx = get_clustermedoids_indeces(
        df.loc[:, ["cluster_assignment","longitude", "latitude"]])
    return df.iloc[medoids_idx,:]
