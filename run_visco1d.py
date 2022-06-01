import matplotlib.pyplot as plt
import numpy as np
import IPython
import argparse
import os
import uuid
import pandas as pd

# TODO: Replace os.system with subprocess?
VISCO1D_BULK_MODULUS_TO_MKS_BULK_MODULUS = 1e10
VISCO1D_SHEAR_MODULUS_TO_MKS_SHEAR_MODULUS = 1e10
VISCO1D_VISCOSITY_TO_MKS_VISCOSITY = 1e18
DPI_PNG = 500


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

    # Read earth.model Layers
    # Maxwell only case columns:
    # bottom_radius",
    #         "top_radius",
    #         "density",
    #         "bulk_modulus",
    #         "shear_modulus",
    #         "maxwell_viscosity",
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
            "to_process_1",  # Could be Maxwell viscosity or Kelvin shear modulus
            "to_process_2",  # First column present if Burgers layer
            "to_process_3",  # First column present if Burgers layer
            "to_process_4",  # First column present if Burgers layer
        ],
    )

    # Are there any Burgers rheology layers
    any_burgers_layers = ~earth_model["data"]["to_process_2"].isnull().values.any()
    if any_burgers_layers:
        pass
    else:
        earth_model["data"]["maxwell_viscosity"] = earth_model["data"]["to_process_1"]

    # Physical and useful derived parameters
    # bottom_radius: km
    # top_radius: km
    # density: g / cm**3
    # bulk modulus: 10**10 Pa
    # shear modulus:10**10 Pa
    # viscosity: 10**18 Pa s
    earth_model["data"]["bulk_modulus_mks"] = (
        earth_model["data"]["shear_modulus"] * VISCO1D_BULK_MODULUS_TO_MKS_BULK_MODULUS
    )
    earth_model["data"]["shear_modulus_mks"] = (
        earth_model["data"]["shear_modulus"]
        * VISCO1D_SHEAR_MODULUS_TO_MKS_SHEAR_MODULUS
    )
    earth_model["data"]["maxwell_viscosity_mks"] = (
        earth_model["data"]["maxwell_viscosity"] * VISCO1D_VISCOSITY_TO_MKS_VISCOSITY
    )
    earth_model["data"]["maxwell_viscosity_mks_log10"] = np.log10(
        earth_model["data"]["maxwell_viscosity_mks"]
    )
    return earth_model


def plot_earth_model(earth_model, output_folder_name):
    # Plot earth model

    def plot_radius_subplot(earth_model, key, x_label_text):
        for i in range(len(earth_model["data"])):
            plt.fill(
                [
                    0,
                    0,
                    earth_model["data"][key][i],
                    earth_model["data"][key][i],
                ],
                [
                    earth_model["data"]["bottom_radius"][i],
                    earth_model["data"]["top_radius"][i],
                    earth_model["data"]["top_radius"][i],
                    earth_model["data"]["bottom_radius"][i],
                ],
                "b",
            )
        plt.xlabel(x_label_text)
        plt.ylabel("radius (km)")

    plt.figure(figsize=(15, 5))
    plt.subplot(1, 4, 1)
    plot_radius_subplot(earth_model, "density", "density (g/cm^3)")

    plt.subplot(1, 4, 2)
    plot_radius_subplot(earth_model, "bulk_modulus_mks", "bulk modulus (Pa)")

    plt.subplot(1, 4, 3)
    plot_radius_subplot(earth_model, "shear_modulus_mks", "shear modulus (Pa)")

    plt.subplot(1, 4, 4)
    plot_radius_subplot(
        earth_model,
        "maxwell_viscosity_mks_log10",
        "log10 Maxwell viscosity (Pa s)",
    )

    plt.savefig(os.path.join(output_folder_name, "earth_model.png"), dpi=DPI_PNG)
    plt.savefig(os.path.join(output_folder_name, "earth_model.pdf"))
    plt.close()
    plt.show(block=True)


def main():
    plt.close("all")

    # Create output folder name:
    output_folder_name = os.path.join("./output/", str(uuid.uuid4().hex))
    print(output_folder_name)
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)

    earth_model_file_name = "./data/earth.modelMAXWELL"
    earth_model = read_earth_model(earth_model_file_name)
    plot_earth_model(earth_model, output_folder_name)

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
