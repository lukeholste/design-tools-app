# Bolted Joint Analyzer

A Streamlit web application for analyzing and visualizing bolted joints in mechanical engineering applications.

## Features

- Interactive selection of bolt sizes, threads per inch (TPI), and materials
- Support for multiple member configurations with different materials and thicknesses
- Clearance hole calculations
- Visual representation of bolted joint assemblies
- Engineering calculations for bolt stiffness and joint properties

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

Navigate to the provided local URL (typically `http://localhost:8501`) to use the application.

## Application Components

- **Bolt Parameters**: Select bolt size, TPI, and material from engineering databases
- **Member Configuration**: Define thickness and material properties for joint members
- **Visualization**: Real-time 2D visualization of the bolted joint assembly
- **Analysis**: Calculate grip length, bolt stiffness, and other joint properties

## Data Files

The application uses JSON data files containing:
- `bolt_sizes.json`: Standard bolt dimensions and thread specifications
- `materials.json`: Material properties (Young's modulus, yield strength, Poisson's ratio)
- `clearance_holes.json`: Standard clearance hole dimensions

## File Structure

- `app.py`: Main Streamlit application
- `classes.py`: Core classes for Bolt, Washer, Member, and BoltedJoint
- `plotter.py`: Visualization functions using matplotlib
- `resources.py`: Data loading utilities
- `data/`: JSON files with engineering data