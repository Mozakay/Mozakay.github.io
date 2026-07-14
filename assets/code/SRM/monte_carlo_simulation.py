import numpy as np

SEED = 42
N_ITERATIONS = 10_000


RISKS = {
    "R1 Inventory data inaccuracy": dict( mn=0.40, ml=0.55, mx=0.65, impact=4, areas=("availability",)),

    "R2 System integration failure": dict( mn=0.20, ml=0.35, mx=0.50, impact=4, areas=("availability", "quality")),

    "R3 Cybersecurity breach / ransomware": dict( mn=0.10, ml=0.20, mx=0.35, impact=5, areas=("availability", "security")),

    "R4 International supplier/logistics disruption and quality variation": dict( mn=0.20, ml=0.35, mx=0.50, impact=5, areas=("quality", "availability")),

    "R5 Automated warehouse system failure": dict( mn=0.10, ml=0.20, mx=0.35, impact=4, areas=("availability", "quality")),
}

# Outcomes aligned with the assignment focus
OUTCOMES = ["quality", "availability", "security"]


def validate_inputs():
    """Check that probability and impact assumptions are valid."""

    for name, r in RISKS.items():
        mn, ml, mx = r["mn"], r["ml"], r["mx"]

        if not (0 <= mn <= ml <= mx <= 1):
            raise ValueError(
                f"Invalid probability values for {name}: "
                "expected 0 <= Min <= Most Likely <= Max <= 1."
            )

        if not (1 <= r["impact"] <= 5):
            raise ValueError(
                f"Invalid impact value for {name}: impact must be between 1 and 5."
            )

        for area in r["areas"]:
            if area not in OUTCOMES:
                raise ValueError(
                    f"Invalid outcome area '{area}' in {name}. "
                    f"Allowed outcomes are: {OUTCOMES}."
                )


def risk_probability_table():
    """Model Output 1: Expected probability and exposure for each individual risk."""

    print("\nTable Output 1: Risk assumptions and expected exposure")
    print(f"{'Risk':70s}{'Mean probability':>18s}{'Impact':>8s}{'Expected exposure':>20s}")

    for name, r in RISKS.items():
        mean_probability = (r["mn"] + r["ml"] + r["mx"]) / 3
        expected_exposure = mean_probability * r["impact"]

        print(
            f"{name:70s}"
            f"{mean_probability * 100:>17.1f}%"
            f"{r['impact']:>8d}"
            f"{expected_exposure:>20.2f}"
        )


def probability_impact_ranking():
    """Model Output 2: Ranking using the most likely probability only."""


    rows = []

    for name, r in RISKS.items():
        exposure = r["ml"] * r["impact"]
        rows.append((name, r["ml"], r["impact"], exposure))

    rows.sort(key=lambda x: x[3], reverse=True)

    print("\nTable Output 2: Probability x Impact ranking")
    print(
        f"{'Risk':<72}"
        f"{'Most likely':>13}"
        f"{'Impact':>10}"
        f"{'Exposure':>12}"
    )

    for name, ml, impact, exposure in rows:
        print(
            f"{name:<72}"
            f"{ml * 100:>12.0f}%"
            f"{impact:>10d}"
            f"{exposure:>12.2f}"
        )

    return rows


def run_simulation(seed=SEED, n=N_ITERATIONS):
    """Monte Carlo simulation using triangular distributions for each risk."""

    rng = np.random.default_rng(seed)

    samples = {
        name: rng.triangular(r["mn"], r["ml"], r["mx"], n)
        for name, r in RISKS.items()
    }

    distributions = {}

    for outcome in OUTCOMES:
        keys = [name for name, r in RISKS.items() if outcome in r["areas"]]

        prob_none = np.ones(n)

        for k in keys:
            prob_none *= 1 - samples[k]

        distributions[outcome] = 1 - prob_none

    return distributions


def summarize_simulation(distributions):
    """Model Output 3: Mean and 5th/95th percentile for each outcome."""


    print("\nTable Output 3: Monte Carlo simulation results")
    print(f"{'Outcome':38s}{'Mean':>10s}{'5th pct':>10s}{'95th pct':>10s}")

    labels = {
        "quality": "At least one quality issue",
        "availability": "At least one availability issue",
        "security": "At least one security issue",
    }

    results = {}

    for outcome in OUTCOMES:
        dist = distributions[outcome]

        mean = dist.mean() * 100
        p5 = np.percentile(dist, 5) * 100
        p95 = np.percentile(dist, 95) * 100

        results[outcome] = (mean, p5, p95)

        print(f"{labels[outcome]:38s}{mean:>9.1f}%{p5:>9.1f}%{p95:>9.1f}%")

    return results


def deterministic_crosscheck():
    """Table Output 4: Deterministic cross-check using most likely probabilities."""

    print("\nTable Output 4: Deterministic cross-check")
    print(f"{'Outcome':38s}{'Result':>10s}")

    labels = {
        "quality": "At least one quality issue",
        "availability": "At least one availability issue",
        "security": "At least one security issue",
    }

    for outcome in OUTCOMES:
        keys = [name for name, r in RISKS.items() if outcome in r["areas"]]

        prob_none = 1.0

        for k in keys:
            prob_none *= 1 - RISKS[k]["ml"]

        result = (1 - prob_none) * 100

        print(f"{labels[outcome]:38s}{result:>9.1f}%")


if __name__ == "__main__":
    validate_inputs()

    risk_probability_table()
    probability_impact_ranking()

    distributions = run_simulation()
    summarize_simulation(distributions)

    deterministic_crosscheck()

    print(f"\n[seed={SEED}, iterations={N_ITERATIONS:,}]")