"""Trait scores for the five most-searched breeds, plus the average of all 67 breeds.
Output: data/traits_favourites.csv (one row per breed and trait)."""
import pandas as pd

traits = pd.read_csv("data/traits_long.csv")
favourites = ["Ragdoll", "Maine Coon", "British Shorthair", "Bengal", "Persian"]

fav = traits[traits["name"].isin(favourites)][["name", "trait", "trait_order", "score"]]

avg = traits.groupby(["trait", "trait_order"], as_index=False)["score"].mean().round(1)
avg["name"] = "Average of all 67 breeds"

out = pd.concat([fav, avg[["name", "trait", "trait_order", "score"]]])
out.to_csv("data/traits_favourites.csv", index=False)
print(out.pivot(index="name", columns="trait", values="score"))
