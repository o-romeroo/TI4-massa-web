import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colrs
import scipy.cluster.hierarchy as sch
from kmodes import kmodes
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.services.ResultService import ResultService

def numerical_number_of_clusters(distances_list):
    # Elbow method using the Euclidean distance:
    shorted_list = distances_list[0:21]  # Create a list of distances from the first 21 clusters.
    x1, y1 = 1, shorted_list[0]  # Define the x-axis coordinates of the first and last points on the line.
    x2, y2 = len(shorted_list) - 1, shorted_list[
        len(shorted_list) - 1]  # Define the y-axis coordinates of the first and last points on the line.
    distances = []
    for i in range(len(shorted_list)):
        x0 = i + 1  # Coordinate on the x-axis of the point to calculate the distance to the line.
        y0 = shorted_list[i]  # Coordinate on the y-axis of the point to calculate the distance to the line.
        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** (1 / 2)
        distances.append(numerator / denominator)  # Distance between a point and a line.
    return (distances.index(max(distances)) + 1)


def categorical_number_of_clusters(file):
    # Elbow method using the clustering cost:
    listClusCosts = []
    for n in range(2, 21):  # Calculate the cost for each n cluster.
        km = kmodes.KModes(n_clusters=n, verbose=0, n_init=20, init='Cao', max_iter=300)
        km.fit(X=file)
        listClusCosts.append(
            km.cost_)  # Costs = Clustering cost, defined as the sum distance of all points to their respective cluster centroids.
    x1, y1 = 2, listClusCosts[0]  # Define the x-axis coordinates of the first and last points on the line.
    x2, y2 = 20, listClusCosts[
        len(listClusCosts) - 1]  # Define the y-axis coordinates of the first and last points on the line.

    distances = []
    for i in range(len(listClusCosts)):
        x0 = i + 2  # Coordinate on the x-axis of the point to calculate the distance to the line.
        y0 = listClusCosts[i]  # Coordinate on the y-axis of the point to calculate the distance to the line.
        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** (1 / 2)
        distances.append(numerator / denominator)  # Distance between a point and a line.
    return (distances.index(max(distances)) + 2)


async def optimal_threshold(file, ident, extension_type, linkage, result_id, session: AsyncSession):
    distances_list = sch.maxdists(linkage)  # Calculate the maximum distance between clusters.
    distances_list = sorted(list(distances_list))  # Extract and sort the distances in ascending order.
    distances_list.reverse()  # Sort the list in descending order.

    # Calculate the number of clusters
    number_of_clusters = numerical_number_of_clusters(distances_list)
    CutOff = distances_list[number_of_clusters - 2]  # Define the cutoff threshold for the dendrogram

    # Define the title variable and column to be updated, then generate the plot and get the buffer
    if ident == 'bio':
        title_distances = 'Plot of Euclidean Distances from Biological HCA'
        column_table = 'biological_hca_euclidian_distances'
        print('Biological:', number_of_clusters)  # Print the number of clusters for the biological domain
        # Generate the plot and get the buffer
        buffer = plot_euclidean_distance(distances_list, extension_type, title_distances)

    elif ident == 'PhCh':
        title_distances = 'Plot of Euclidean Distances from Physicochemical HCA'
        column_table = 'physicochemical_hca_euclidian_distances'
        print('Physicochemical:', number_of_clusters)  # Print the number of clusters for the physicochemical domain
        # Generate the plot and get the buffer
        buffer = plot_euclidean_distance(distances_list, extension_type, title_distances)

    else:
        title_distances = 'Plot of Euclidean Distances from Structural HCA'
        column_table = 'structural_hca_euclidian_distances'
        print('Structural:', number_of_clusters)  # Print the number of clusters for the structural domain
        # Generate the plot and get the buffer
        buffer = plot_euclidean_distance(distances_list, extension_type, title_distances)

    # Update the database with the plot image
    result_service = ResultService(session)
    try:
        await result_service.update_result(result_id, column_table, buffer)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise RuntimeError(f"Error committing the result update: {str(e)}")

    return CutOff, number_of_clusters, distances_list



def plot_euclidean_distance(distances_list, extension_type, title_distances):  # Plot the graph of Euclidean distances.
    plt.plot(list(range(1, len(distances_list) + 1)), distances_list, '-o', color='black', markersize=4, linewidth=1,
             markeredgewidth=1)  # Initial setting of graph values and parameters.
    plt.ylabel('Euclidean distance')  # Set the y-axis label.
    original_ticks = list((plt.xticks())[0])  # Get the x-axis ticks.
    increase_rate = original_ticks[2]  # Get the x-axis increment.
    list_x = list(range(1, len(distances_list) + 1,
                        int(increase_rate / 2)))  # Create a list to define the new xticks that correspond to double the points compared to the previous one.

    labels_x = [str(x) for x in list_x]  # Create list_x labels

    plt.xticks(list_x, labels_x, fontsize=8)  # Define the new x-ticks and set the font size.
    plt.title(title_distances)  # Define the graph title.
    # Salva a figura no buffer
    buffer = BytesIO()
    plt.savefig(buffer, format=extension_type)  # Armazena a figura no buffer em formato PNG
    buffer.seek(0)  # Reseta o cursor do buffer para o início
    plt.close()  # Close plot.
    return buffer

async def hca_clusters(file, labels, ident, extension_type, linkage_method, result_id, session: AsyncSession):
    # Get the threshold value (CutOff) and the number of clusters:
    linkage = sch.linkage(file, method=linkage_method, optimal_ordering=False)
    CutOff, number_of_clusters, distances_list = await optimal_threshold(file, ident, extension_type, linkage, result_id, session)

    # Get the cluster labels:
    leaves_cluster = sch.fcluster(linkage, t=number_of_clusters, criterion='maxclust')
    cluster_dict = dict(zip(labels, list(leaves_cluster)))

    return leaves_cluster, cluster_dict, linkage, CutOff, distances_list



async def hca_plot(linkage, labels, leaves_cluster, CutOff, ident, extension_type, dendrogram_xfont_size,
             index_of_test_molecules, result_id, session: AsyncSession):
    # Create an arrow for molecules in test set:
    labels_arrow = labels.copy()
    for i in range(0, len(labels_arrow)):
        if labels_arrow[i] in index_of_test_molecules:
            labels_arrow[i] = ('→ ' + labels_arrow[i])

    # Working with colors:
    hexRGB = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
              '#17becf', '#691605', '#b3f084', '#ffee00', '#00ff6e', '#0400ff', '#c4c4c0', '#ff00fb', '#290e0e',
              '#12290e', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf', '#691605', '#b3f084', '#ffee00', '#00ff6e', '#0400ff', '#c4c4c0', '#ff00fb',
              '#290e0e',
              '#12290e']  # Definition of which colors (colorblind friendly) will be used for each cluster (1-19).
    sch.set_link_color_palette(hexRGB)  # Set hexRGB as the dendrogram colors.

    # Initial setting of HCA dendrograms:
    plt.figure(figsize=(20, 10), dpi=300)  # Set the image space.
    dendrogram = sch.dendrogram(linkage, color_threshold=CutOff, above_threshold_color='k', labels=labels_arrow,
                                get_leaves=True)

    # Set graphs font size for both axis and adjust the plot in image space:
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=dendrogram_xfont_size)
    plt.ylabel('Euclidean distance', fontsize=12)
    plt.subplots_adjust(left=0.06, right=0.96)

    # Set new scale for y axis (which is 2x the number of points in the previous scale):
    b = [float(i) for i in plt.yticks()[0]]
    scale = b[1] - b[0]
    new_scale = scale / 2
    new_arange = np.arange(min(b) - scale / 20, max(b) + new_scale, new_scale)
    plt.yticks(new_arange)

    # Add ticks to x-axis:
    plt.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True)

    # Assign the wrong legend to each cluster:
    set__leaves_cluster = sorted(list(set(leaves_cluster)))
    legend_value = plt.legend(set__leaves_cluster)

    # Get the color for each molecule:
    color_list = list(dendrogram['leaves_color_list'])
    ivl_list = list(dendrogram['ivl'])
    dictionary_of_clusters = dict(zip(labels, leaves_cluster))
    for i in range(0, len(ivl_list)):
        if '→ ' in ivl_list[i]:
            ivl_list[i] = ivl_list[i].replace('→ ', '')
    dictionary_of_colors = dict(zip(ivl_list, color_list))

    # Get the right cluster colors:
    list_cluster_color = []
    for i in dictionary_of_clusters.keys():
        list_cluster_color.append([i, dictionary_of_clusters[i], dictionary_of_colors[i]])

    list_cluster_color = sorted(list_cluster_color, key=lambda x: x[1])
    lcc1 = {}

    if ('k' in color_list) or ('#000000' in color_list):
        lcc1['#000000'] = []

    for i in range(0, len(list_cluster_color)):
        if list_cluster_color[i][2] == 'k':
            lcc1['#000000'].append(list_cluster_color[i][1])
        else:
            lcc1[list_cluster_color[i][2]] = []
            lcc1[list_cluster_color[i][2]].append(list_cluster_color[i][1])

    right_legend = []
    for i in range(0, len(legend_value.get_lines())):
        right_legend.append(colrs.to_hex(legend_value.get_lines()[i].get_color()))

    # Assign the right legend to each cluster:
    set_leaves_cluster = []
    for i in right_legend:
        if (len(lcc1[i])) > 1:
            c_name = ''
            for z in range(0, len(lcc1[i])):
                a = lcc1[i][z]
                if z == len(lcc1[i]) - 1:
                    if a < 10:
                        c_name += 'cluster 0' + str(a) + ' (outliers)'
                    else:
                        c_name += 'cluster ' + str(a) + ' (outliers)'
                else:
                    if a < 10:
                        c_name += 'cluster 0' + str(a) + ', '
                    else:
                        c_name += 'cluster ' + str(a) + ', '
            set_leaves_cluster.append(c_name)
        else:
            a = int(list(set(lcc1[i]))[0])
            if a < 10:
                c_name = 'cluster 0' + str(a)
                set_leaves_cluster.append(c_name)
            else:
                c_name = 'cluster ' + str(a)
                set_leaves_cluster.append(c_name)
    legend_value = plt.legend(set_leaves_cluster)

    # Apply cluster color to x-labels:
    zip_label_color = list(zip(plt.gca().get_xticklabels(), color_list))
    for i, a in zip_label_color:
        i.set_color(a)

    # Define the title of the graph and saves the figure:
    buffer = BytesIO()
    if ident == 'bio':
        plt.title('HCA of biological activity')
        plt.savefig(buffer, format=extension_type)
        buffer.seek(0)
        column_table = 'biological_activity_hca'

    elif ident == 'PhCh':
        plt.title('HCA of physicochemical properties')
        plt.savefig(buffer, format=extension_type)
        buffer.seek(0)
        column_table = 'physicochemical_properties_hca'
    else:
        plt.title('HCA of AtomPairs fingerprint')
        plt.savefig(buffer, format=extension_type)
        buffer.seek(0)
        column_table = 'atom_pairs_fingerprint_hca'

    plt.close()

    # Update the database with the plot image
    result_service = ResultService(session)
    await result_service.update_result(result_id, column_table, buffer)
    await session.commit()
    


def kmodes_clusters(file, names):
    # Calculate the number of clusters for the Kmodes:
    n_clusters = categorical_number_of_clusters(file)
    print('General:', n_clusters)  # Print the number of clusters.

    # Run Kmodes with the calculated number of clusters:
    km_test = kmodes.KModes(n_clusters=n_clusters, n_init=20, init='Cao', max_iter=300)  # Parameter setting.
    clusters = km_test.fit_predict(
        file)  # Run Kmodes for the dataset and return an array with cluster labels for each molecule.
    clusters_list = list(clusters)  # Transform np.array into a list.

    # Create a dictionary with the pair "molecule name": "General cluster ID":
    HCA_General_dict = {}
    for i, a in zip(names, clusters_list):
        HCA_General_dict[i] = int(a + 1)
    return HCA_General_dict