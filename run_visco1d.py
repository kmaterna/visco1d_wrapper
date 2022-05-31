import matplotlib.pyplot as plt
import numpy as np
import IPython
import argparse
import os
import pandas as pd

# TODO: Replace os.system with subprocess?


def read_earth_model(earth_model_file_name):
    # Read earth model
    earth_model = {}
    earth_model["file_name"] = earth_model_file_name

    with open(earth_model["file_name"]) as f:
        first_line_values = f.readline().strip().split()
        earth_model["n_layers"] = int(first_line_values[0])
        earth_model["n_ve_layers"] = int(first_line_values[1])
        earth_model["radius"] = float(first_line_values[2])
        earth_model["depfac"] = float(first_line_values[3])

    earth_model["data"] = pd.read_csv(
        earth_model["file_name"],
        delim_whitespace=True,
        skiprows=1,
        names=[
            "bottom_radius",
            "top_radius",
            "density",
            "bulk_modulus",
            "shear_modulus",
            "viscosity",
        ],
    )

    # Physical and useful derived parameters
    # bottom_radius: km
    # top_radius: km
    # density: g / cm**3
    # bulk modulus: 10**10 Pa
    # shear modulus:10**10 Pa
    # viscosity: 10**18 Pa s
    earth_model["data"]["bulk_modulus_physical"] = (
        earth_model["data"]["shear_modulus"] * 1e10
    )
    earth_model["data"]["shear_modulus_physical"] = (
        earth_model["data"]["shear_modulus"] * 1e10
    )
    earth_model["data"]["viscosity_physical"] = earth_model["data"]["viscosity"] * 1e18
    earth_model["data"]["viscosity_physical_log10"] = np.log10(
        earth_model["data"]["viscosity_physical"]
    )
    return earth_model


def plot_earth_model(earth_model):
    # Plot earth model
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 4, 1)
    for i in range(len(earth_model["data"])):
        plt.fill(
            [
                0,
                0,
                earth_model["data"]["density"][i],
                earth_model["data"]["density"][i],
            ],
            [
                earth_model["data"]["bottom_radius"][i],
                earth_model["data"]["top_radius"][i],
                earth_model["data"]["top_radius"][i],
                earth_model["data"]["bottom_radius"][i],
            ],
            "b",
        )
    plt.xlabel("density (g/cm^3)")
    plt.ylabel("radius (km)")

    plt.subplot(1, 4, 2)
    for i in range(len(earth_model["data"])):
        plt.fill(
            [
                0,
                0,
                earth_model["data"]["bulk_modulus_physical"][i],
                earth_model["data"]["bulk_modulus_physical"][i],
            ],
            [
                earth_model["data"]["bottom_radius"][i],
                earth_model["data"]["top_radius"][i],
                earth_model["data"]["top_radius"][i],
                earth_model["data"]["bottom_radius"][i],
            ],
            "b",
        )
    plt.xlabel("bulk modulus (Pa)")
    # plt.ylabel("radius (km)")

    plt.subplot(1, 4, 3)
    for i in range(len(earth_model["data"])):
        plt.fill(
            [
                0,
                0,
                earth_model["data"]["shear_modulus_physical"][i],
                earth_model["data"]["shear_modulus_physical"][i],
            ],
            [
                earth_model["data"]["bottom_radius"][i],
                earth_model["data"]["top_radius"][i],
                earth_model["data"]["top_radius"][i],
                earth_model["data"]["bottom_radius"][i],
            ],
            "b",
        )
    plt.xlabel("shear modulus (Pa)")
    # plt.ylabel("radius (km)")

    plt.subplot(1, 4, 4)
    for i in range(len(earth_model["data"])):
        plt.fill(
            [
                0,
                0,
                earth_model["data"]["viscosity_physical_log10"][i],
                earth_model["data"]["viscosity_physical_log10"][i],
            ],
            [
                earth_model["data"]["bottom_radius"][i],
                earth_model["data"]["top_radius"][i],
                earth_model["data"]["top_radius"][i],
                earth_model["data"]["bottom_radius"][i],
            ],
            "b",
        )
    plt.xlabel("log10 Maxwell viscosity (Pa s)")
    # plt.ylabel("radius (km)")

    plt.show(block=True)


def main():
    plt.close("all")
    earth_model_file_name = "./data/earth.modelMAXWELL"
    earth_model = read_earth_model(earth_model_file_name)
    plot_earth_model(earth_model)

    print(earth_model["data"])

    # success = os.system(f"cp {earth_model['file_name']} earth.model")

    # cp earth.modelHOMO30 earth.model
    # nice decay4m <<! > /dev/null
    # 2 1500
    # !
    # nice vsphm <<! > /dev/null 10.
    # !
    # nice decay <<! > /dev/null 2 1500
    # !
    # nice vtordep <<! > /dev/null
    # 10.
    # !
    # nice strainA < strainx.inTHRUST > /dev/null mv strainA.out strainA.outTHRUSTg

    IPython.embed(banner1="")


if __name__ == "__main__":
    # TODO: add argument parsing
    main()
