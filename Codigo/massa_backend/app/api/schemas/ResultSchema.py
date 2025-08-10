from typing import Dict, Optional, List, Union
from pydantic import BaseModel, Field


class ResultOutput(BaseModel):
    id: int
    execution_id: int
    biological_hca_euclidian_distances: Optional[bytes] = None
    physicochemical_hca_euclidian_distances: Optional[bytes] = None
    structural_hca_euclidian_distances: Optional[bytes] = None
    biological_clustering_dataset_dist: Optional[bytes] = None
    structural_clustering_dataset_dist: Optional[bytes] = None
    physicochemical_clustering_dataset_dist: Optional[bytes] = None
    general_clustering_dataset_dist: Optional[bytes] = None
    biological_activity_hca: Optional[bytes] = None
    physicochemical_properties_hca: Optional[bytes] = None
    atom_pairs_fingerprint_hca: Optional[bytes] = None


class ResultInput(BaseModel):
    execution_id: int
    biological_hca_euclidian_distances: Optional[bytes] = None
    physicochemical_hca_euclidian_distances: Optional[bytes] = None
    structural_hca_euclidian_distances: Optional[bytes] = None
    biological_clustering_dataset_dist: Optional[bytes] = None
    structural_clustering_dataset_dist: Optional[bytes] = None
    physicochemical_clustering_dataset_dist: Optional[bytes] = None
    general_clustering_dataset_dist: Optional[bytes] = None
    biological_activity_hca: Optional[bytes] = None
    physicochemical_properties_hca: Optional[bytes] = None
    atom_pairs_fingerprint_hca: Optional[bytes] = None



#graphic data

class DistancePlotsOutput(BaseModel):
    title: str = Field(description="Title")
    x: List[int] = Field(description="X-axis values (indices)")
    y: List[Union[float, int]] = Field(description="Y-axis values (distances)")

class DistributionPlotsOutput(BaseModel):
    title: str = Field(description="Title")
    labels: List[str] = Field(description="Cluster labels")
    total: List[float] = Field(description="Percentage of each cluster in the total set")
    training_set: List[float] = Field(description="Percentage of each cluster in the training set")
    test_set: List[float] = Field(description="Percentage of each cluster in the test set")

class GraphicsOutput(BaseModel):
    dendrograms: Dict[str, Optional[str]] = {}
    distance_plot: Dict[str, Optional[DistancePlotsOutput]] = {}
    distribution_plots: Dict[str, Optional[DistributionPlotsOutput]] = {}


# Images base64
class ImagesOutput(BaseModel):
    dendrograms: Dict[str, Optional[str]] = {}
    distance_plots: Dict[str, Optional[str]] = {}
    distribution_plots: Dict[str, Optional[str]] = {}

# Response
class ResultStartOutput(BaseModel):
    message: str
    images: Union[ImagesOutput, GraphicsOutput]