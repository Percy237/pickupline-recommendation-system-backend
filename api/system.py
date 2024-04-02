from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import cross_validate

# Load data from the ratings JSON
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[["user_id", "pickup_line_id", "rating"]], reader)

# Use user-based collaborative filtering with KNN
sim_options = {
    "name": "cosine",
    "user_based": True,  # compute similarities between users
}
algo = KNNBasic(sim_options=sim_options)

# Perform cross-validation
cross_validate(algo, data, measures=["RMSE", "MAE"], cv=5, verbose=True)
