### Wrapper for Visco1d

Visco1D (Pollitz, 1997) computes the time-dependent response of a radially symetric viscoelastic/elastic Earth to imposed fault slip. 

This wrapper uses Python to improve the usability of the Visco1D code. 

### Highly speculative draft of approximate flow control

```mermaid
flowchart TD
  classDef function fill:#f96;
  subgraph visco1d_wrapper
    build_earth_model:::function-->build_fault_model:::function-->run_decay:::function-->run_strain:::function
    build_earth_model:::function-->earth_model
    build_fault_model:::function-->latlon.inDEF???
    earth_model-->run_decay
    latlon.inDEF???-->run_strain
    run_strain-->spherical_harmonic_coefficients???
    spherical_harmonic_coefficients???-->interpolate_to_observation_coordinates?:::function
    interpolate_to_observation_coordinates?:::function-->plot_displacments_and_time_series:::function
    plot_displacments_and_time_series:::function-->many_plots.pdf
  end
```

#### References

Pollitz, Fred F. "Gravitational viscoelastic postseismic relaxation on a layered spherical Earth." Journal of Geophysical Research: Solid Earth 102.B8 (1997): 17921-17941.
