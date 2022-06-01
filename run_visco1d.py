import matplotlib.pyplot as plt
import numpy as np
import IPython
import argparse
import os
import uuid
import pandas as pd
import shutil

# TODO: Replace os.system with subprocess?

# Unit conversion constants
KM_TO_M = 1e3
CGS_DENSITY_TO_MKS_DENSITY = 1e3
VISCO1D_BULK_MODULUS_TO_MKS_BULK_MODULUS = 1e10
VISCO1D_SHEAR_MODULUS_TO_MKS_SHEAR_MODULUS = 1e10
VISCO1D_VISCOSITY_TO_MKS_VISCOSITY = 1e18

# Figure constants
DPI_PNG = 500


def read_earth_model(earth_model_file_name):
    """
    Read earth model layers

    Maxwell rheology columns:
    1. bottom_radius
    2. top_radius
    3. density
    4. bulk_modulus
    5. maxwell_shear_modulus
    6. maxwell_viscosity

    Kelvin rheology columns:
    1. bottom_radius
    2. top_radius
    3. density
    4. bulk_modulus
    5. maxwell_shear_modulus
    6. kelvin_shear_modulus
    7. maxwell_viscosity
    8. kelvin_viscosity
    """

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
            "maxwell_shear_modulus",
            "to_process_1",  # Could be Maxwell viscosity or Kelvin shear modulus
            "to_process_2",  # First column present if Burgers layer
            "to_process_3",  # First column present if Burgers layer
        ],
    )

    # Process layers with Burgers rheology
    earth_model["data"]["maxwell_viscosity"] = 0.0
    earth_model["data"]["kelvin_shear_modulus"] = 0.0
    earth_model["data"]["kelvin_viscosity"] = 0.0
    any_burgers_layers = ~earth_model["data"]["to_process_2"].isnull().values.all()
    if any_burgers_layers:
        print("Found Burgers layers")
        for i in range(len(earth_model["data"])):
            if np.isnan(earth_model["data"]["to_process_2"][i]):
                earth_model["data"]["maxwell_viscosity"].values[i] = earth_model[
                    "data"
                ]["to_process_1"].values[i]
                earth_model["data"]["kelvin_shear_modulus"].values[i] = np.nan
                earth_model["data"]["kelvin_viscosity"].values[i] = 0
            else:
                earth_model["data"]["kelvin_shear_modulus"].values[i] = earth_model[
                    "data"
                ]["to_process_1"].values[i]
                earth_model["data"]["maxwell_viscosity"].values[i] = earth_model[
                    "data"
                ]["to_process_2"].values[i]
                earth_model["data"]["kelvin_viscosity"].values[i] = earth_model["data"][
                    "to_process_3"
                ].values[i]
    else:
        print("Found only Maxwell layers")
        earth_model["data"]["maxwell_viscosity"] = earth_model["data"]["to_process_1"]
        earth_model["data"]["kelvin_shear_modulus"] = np.nan
        earth_model["data"]["kelvin_viscosity"] = np.nan

    # Convert visco1d dimensions to MKS
    earth_model["data"]["top_radius_mks"] = earth_model["data"]["top_radius"] * KM_TO_M
    earth_model["data"]["bottom_radius_mks"] = (
        earth_model["data"]["bottom_radius"] * KM_TO_M
    )
    earth_model["data"]["density_mks"] = (
        earth_model["data"]["density"] * CGS_DENSITY_TO_MKS_DENSITY
    )
    earth_model["data"]["bulk_modulus_mks"] = (
        earth_model["data"]["maxwell_shear_modulus"]
        * VISCO1D_BULK_MODULUS_TO_MKS_BULK_MODULUS
    )
    earth_model["data"]["maxwell_shear_modulus_mks"] = (
        earth_model["data"]["maxwell_shear_modulus"]
        * VISCO1D_SHEAR_MODULUS_TO_MKS_SHEAR_MODULUS
    )
    earth_model["data"]["kelvin_shear_modulus_mks"] = (
        earth_model["data"]["kelvin_shear_modulus"]
        * VISCO1D_SHEAR_MODULUS_TO_MKS_SHEAR_MODULUS
    )
    earth_model["data"]["maxwell_viscosity_mks"] = (
        earth_model["data"]["maxwell_viscosity"] * VISCO1D_VISCOSITY_TO_MKS_VISCOSITY
    )
    earth_model["data"]["maxwell_viscosity_mks_log10"] = np.log10(
        earth_model["data"]["maxwell_viscosity_mks"]
    )
    earth_model["data"]["kelvin_viscosity_mks"] = (
        earth_model["data"]["kelvin_viscosity"] * VISCO1D_VISCOSITY_TO_MKS_VISCOSITY
    )
    earth_model["data"]["kelvin_viscosity_mks_log10"] = np.log10(
        earth_model["data"]["kelvin_viscosity_mks"]
    )

    # Delete columns that were used for temporary storage
    earth_model["data"].drop(
        columns=["to_process_1", "to_process_2", "to_process_3"], inplace=True
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

    plt.figure(figsize=(20, 5))
    plt.subplot(1, 6, 1)
    plot_radius_subplot(earth_model, "density_mks", "density (kg/m^3)")

    plt.subplot(1, 6, 2)
    plot_radius_subplot(earth_model, "bulk_modulus_mks", "bulk modulus (Pa)")

    plt.subplot(1, 6, 3)
    plot_radius_subplot(
        earth_model, "maxwell_shear_modulus_mks", "Maxwell shear modulus (Pa)"
    )

    plt.subplot(1, 6, 4)
    plot_radius_subplot(
        earth_model,
        "maxwell_viscosity_mks_log10",
        "log10 Maxwell viscosity (Pa s)",
    )

    plt.subplot(1, 6, 5)
    plot_radius_subplot(
        earth_model, "kelvin_shear_modulus_mks", "Kelvin shear modulus (Pa)"
    )

    plt.subplot(1, 6, 6)
    plot_radius_subplot(
        earth_model,
        "kelvin_viscosity_mks_log10",
        "log10 Kelvin viscosity (Pa s)",
    )

    plt.savefig(os.path.join(output_folder_name, "earth_model.png"), dpi=DPI_PNG)
    plt.savefig(os.path.join(output_folder_name, "earth_model.pdf"))
    plt.close()
    plt.show(block=True)


def create_output_folder():
    output_folder_name = os.path.join("./output/", str(uuid.uuid4().hex))
    print(f"Working in and saving results to: {output_folder_name}")
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)
    return output_folder_name


def copy_binaries_to_output_folder(visco1d_binary_folder_name, output_folder_name):
    binaries_to_copy = ["decay", "decay4", "decay4m", "vsphdep", "vsphm", "vtordep"]
    for file_name in binaries_to_copy:
        try:
            shutil.copyfile(
                os.path.join(visco1d_binary_folder_name, file_name),
                os.path.join(output_folder_name, file_name),
            )
            print(f"SUCCESS: Copied {file_name} to working folder")
        except:
            print(f"FAILED to copy {file_name} to working folder")


def main():
    plt.close("all")
    visco1d_binary_folder_name = "./bin_visco1d/"
    earth_model_file_name = "./data/earth.modelMAXWELL"
    # earth_model_file_name = "./data/earth.modelBURG30"
    print(f"Earth structure specified in: {earth_model_file_name}")

    # Create output folder
    output_folder_name = create_output_folder()

    # Copy all visco1d binaries to working folder
    copy_binaries_to_output_folder(visco1d_binary_folder_name, output_folder_name)

    # Read and plot earth model
    earth_model = read_earth_model(earth_model_file_name)
    plot_earth_model(earth_model, output_folder_name)

    # print(earth_model["data"])

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

    # Remove binaries from working folder

    # Drop into ipython REPL
    IPython.embed(banner1="")


if __name__ == "__main__":
    # TODO: add argument parsing
    main()
