### Wrapper for Visco1d

Visco1D (Pollitz, 1997) computes the time-dependent response of a radially symetric viscoelastic/elastic Earth to imposed fault slip. 

This wrapper uses Python to improve the usability of the Visco1D code. 

### Assumed folder structure
```
visco1d_wrapper/
├── README.md
├── bin_visco1d/
│   ├── decay (executable)
│   ├── decay4 (executable)
│   ├── decay4m (executable)
│   ├── vsphdep (executable)
│   ├── vsphm (executable)
│   └── vtordep (executable)
├── data/
│   ├── earth_model_0001
│   ├── earth_model_0002
│   └── etc.
└── output/
    ├── e1024fc284b24705a862523420739de0
    |   ├── earth_model.pdf
    |   ├── earth_model.png
    |   └── strain.out
    └── 8776d972320e439ebd0f1c0b3866c405
        ├── earth_model.pdf
        ├── earth_model.png        
        └── strain.out
```

### Highly speculative draft of approximate flow control

```mermaid
flowchart TD
  classDef function fill:#f96;
  subgraph visco1d_wrapper
    build_earth_model:::function
    build_fault_model:::function-->fault_model-->run_strain:::function
    build_earth_model:::function-->earth_model
    earth_model-->run_decay:::function
    latlon.inDEF-->run_strain:::function
    run_decay-->spherical_harmonic_coefficients
    spherical_harmonic_coefficients-->run_strain
    run_strain-->displacements_at_coords_at_times
    displacements_at_coords_at_times-->plot_displacments_and_time_series:::function
        plot_displacments_and_time_series:::function-->many_plots.pdf
  end
```

#### References

Pollitz, Fred F. "Gravitational viscoelastic postseismic relaxation on a layered spherical Earth." Journal of Geophysical Research: Solid Earth 102.B8 (1997): 17921-17941.
