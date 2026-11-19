"""Run: uv run --with pandas --with statsmodels --with matplotlib lab.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

df: pd.DataFrame = pd.read_csv("Chapter_09_Regression_Lab_Dataset.csv")
FA: str = "units_sold ~ price"
FB: str = "units_sold ~ price + promotion + ad_spend + competitor_price"

#? Task 1: inspect
print("Rows:", len(df))
print("Missing values:", int(df.isna().sum().sum()))
print("Duplicate (week, store, product):", int(df.duplicated(["week", "store_id", "product_id"]).sum()))
print(df.describe().round(2).T)
print("\nUnits sold by promotion:\n", df.groupby("promotion")["units_sold"].describe().round(1))
print("\nMean units by week:\n", df.groupby("week")["units_sold"].mean().round(1))
print("\nMean units by store:\n", df.groupby("store_id")["units_sold"].mean().round(1))

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].scatter(df["price"], df["units_sold"], c=df["promotion"], cmap="coolwarm")
ax[0].set(xlabel="price ($)", ylabel="units_sold", title="Units vs price (red = promotion)")
df.boxplot(column="units_sold", by="promotion", ax=ax[1])
ax[1].set(xlabel="promotion", ylabel="units_sold", title="Units by promotion")
fig.suptitle("")
fig.tight_layout()
fig.savefig("plot1_inspect.png")

#? Task 2: fit on weeks 1-3, test on week 4 (predicting a future week)
train: pd.DataFrame = df[df["week"] <= 3]
test: pd.DataFrame = df[df["week"] == 4]
rmse = lambda m, d: float(np.sqrt(((d["units_sold"] - m.predict(d)) ** 2).mean()))

for name, f in [("Model A", FA), ("Model B", FB)]:
    m = smf.ols(f, data=train).fit()
    print(f"\n{name}: {f}")
    print(pd.DataFrame({"coef": m.params, "95% low": m.conf_int()[0], "95% high": m.conf_int()[1],
                        "p": m.pvalues}).round(3))
    print(f"R2 train = {m.rsquared:.3f}, RMSE train = {rmse(m, train):.2f}, RMSE week 4 = {rmse(m, test):.2f}")

#? Task 3: residuals and influence of Model B on the full data
mb = smf.ols(FB, data=df).fit()
df["fitted"], df["resid"] = mb.fittedvalues, mb.resid
cooks: pd.Series = pd.Series(mb.get_influence().cooks_distance[0], index=df.index)
print("\nModel B on all 80 rows, price coef:", round(mb.params["price"], 2))
print("Top 3 Cook's distance (cutoff 4/n = 0.05):")
print(df.assign(cooks=cooks).nlargest(3, "cooks")[["week", "store_id", "product_id", "units_sold", "promotion", "cooks"]].round(3))

fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].scatter(df["fitted"], df["resid"])
ax[0].axhline(0, color="k")
ax[0].set(xlabel="fitted", ylabel="residual", title="Residuals vs fitted")
df.boxplot(column="resid", by="week", ax=ax[1])
ax[1].set(xlabel="week", ylabel="residual", title="Residuals by week")
df.boxplot(column="resid", by="store_id", ax=ax[2])
ax[2].set(xlabel="store", ylabel="residual", title="Residuals by store")
fig.suptitle("")
fig.tight_layout()
fig.savefig("plot2_residuals.png")

#? Group-aware validation: leave one store out, then leave one product out
for group in ["store_id", "product_id"]:
    errs: dict[str, list[float]] = {"A": [], "B": []}
    for g in df[group].unique():
        tr, te = df[df[group] != g], df[df[group] == g]
        errs["A"].append(rmse(smf.ols(FA, data=tr).fit(), te))
        errs["B"].append(rmse(smf.ols(FB, data=tr).fit(), te))
    print(f"\nLeave-one-{group}-out mean RMSE: A = {np.mean(errs['A']):.2f}, B = {np.mean(errs['B']):.2f}")
