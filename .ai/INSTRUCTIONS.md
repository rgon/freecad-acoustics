
# FreeCAD Acoustics AI Collaboration Guide

This document provides essential context for AI models interacting with this project. Adhering to these guidelines will ensure consistency, maintain code quality, and leverage the full power of the FreeCAD environment.

-----

## 1\. Project Overview & Purpose

  * **Primary Goal:** FreeCAD Acoustics is a collection of tools, delivered as a FreeCAD workbench, for designing advanced loudspeaker components. It aims to provide an open-source workflow for acoustic engineers and DIY enthusiasts.
  * **Core Functionality:** The project focuses on the acoustic design and simulation of components like:
      * Waveguides and horns for compression drivers.
      * Compression chambers for transducers.
      * Loudspeaker enclosures (cabinets).
      * Simulating acoustic and mechanical behavior using the Finite Element Method (FEM), such as modal analysis for cabinet resonances or pressure simulations in waveguides.
  * **Domain:** Acoustics, Mechanical Engineering, Audio Engineering, Computer-Aided Design (CAD).

-----

## 2\. Core Technologies & Stack

  * **Language:** **Python** (\>=3.8)
  * **Primary Framework:** **FreeCAD Python API**. All code must run within the FreeCAD environment.
  * **Key FreeCAD Workbenches & APIs:**
      * `PartDesign` & `Sketcher`: For creating parametric, feature-based 2D and 3D geometry.
      * `Part`: For performing constructive solid geometry (CSG) operations.
      * `FemWorkbench`: For setting up, solving, and post-processing FEM simulations.
      * `TechDraw`: For generating technical drawings of the designed parts.
  * **Key Python Libraries:**
      * `PySide`/`PyQt`: For creating custom user interfaces, dialogs, and task panels within FreeCAD.
      * `NumPy` & `SciPy`: For numerical calculations, data analysis, and implementing acoustic formulas.
      * `matplotlib`: For plotting simulation results or other data.
  * **External Dependencies:**
      * **FEM Solvers:** The project will primarily interface with solvers supported by FreeCAD's FEM Workbench, such as **CalculiX** (for structural analysis) and **Elmer** (for acoustics and multiphysics). Users will need to install these separately.
  * **Installation Method:** Deployed as a FreeCAD Addon, either manually by placing it in the `Mod` directory or through the FreeCAD **Addon Manager**.

-----

## 3\. Architectural Patterns

  * **Overall Architecture:** The project is a **Workbench** for FreeCAD. This is an event-driven, plugin-style architecture where our Python code adds new tools and objects that integrate directly into the FreeCAD GUI and modeling kernel.
  * **Directory Structure Philosophy (Standard FreeCAD Workbench):**
    ```
    FreeCAD-Acoustics/
    ├── Init.py             # Module initialization script
    ├── InitGui.py          # GUI initialization, creates the workbench and commands
    ├── icons/              # SVG icons for toolbars and commands
    ├── modules/            # Core Python modules containing the logic
    │   ├── geometry.py     # Functions for creating acoustic geometry (waveguides, etc.)
    │   ├── fem_setup.py    # Functions for automating FEM analysis setup
    │   └── ui_panels.py    # PySide classes for GUI task panels
    └── package.xml         # Metadata for the FreeCAD Addon Manager
    ```
  * **Core Architectural Components:**
    1.  **Parametric Scripted Objects:** Custom Python classes that define new object types in FreeCAD. These objects have properties (e.g., `ThroatDiameter`, `CutoffFrequency`) that can be edited in the Property Editor, and their geometry automatically updates when a property changes. This is the **most important pattern**.
    2.  **GUI Commands:** Classes that define user-facing tools, which appear as buttons in the workbench toolbar. Each command typically creates a scripted object or performs an action on the document.
    3.  **Task Panels:** Custom UI widgets that appear in FreeCAD's Combo View to guide the user through creating or editing an object.
    4.  **FEM Automation Layer:** A set of helper functions that simplify the process of creating FEM analyses for acoustic parts (e.g., applying correct materials, boundary conditions for air, and meshing presets).

-----

## 4\. Coding Conventions & Style Guide

  * **Formatting & Linting:**
      * **Python:** Follows **PEP 8**. Use **`black`** for code formatting and **`ruff`** for linting to maintain a consistent style.
  * **Naming Conventions:**
      * **Python:** `snake_case` for variables and functions, `PascalCase` for classes.
      * **FreeCAD Objects:** User-visible labels should be clear and descriptive (e.g., "OS Waveguide"). Internal object names should use `PascalCase` (e.g., `WaveguideObject`).
  * **FreeCAD Best Practices:**
      * **Parametric & Non-Destructive:** All modeling operations should be parametric. Avoid operations that break the user's model history. Always link new geometry to existing features where appropriate.
      * **Recompute Robustness:** Ensure that objects and their dependencies correctly recalculate when a parameter is changed (`obj.recompute()`).
      * **Use Expressions:** Where possible, use FreeCAD's expression engine to link object properties together instead of hardcoding values in Python.
  * **Scripted Object Pattern Example:**
    This is a simplified example of a scripted object that creates a basic horn.
    ```python
    # In a module like modules/geometry.py

    import FreeCAD as App
    import Part

    class Horn:
        def __init__(self, obj):
            """
            Constructor for the Horn scripted object.
            'obj' is the FreeCAD document object that this class is attached to.
            """
            obj.Proxy = self
            # Define parametric properties
            obj.addProperty("App::PropertyLength", "ThroatDiameter", "Horn", "Diameter of the horn throat").ThroatDiameter = "25.4mm"
            obj.addProperty("App::PropertyFloat", "FlareConstant", "Horn", "Flare constant (m) for the exponential horn").FlareConstant = 0.5
            obj.addProperty("App::PropertyLength", "Length", "Horn", "Length of the horn").Length = "150mm"

        def execute(self, obj):
            """
            Called on recompute. This is where the geometry is built.
            """
            # Access properties using obj.<PropertyName>
            throat_radius = obj.ThroatDiameter.Value / 2.0
            m = obj.FlareConstant
            length = obj.Length.Value

            # Example: Create a simple conical horn shape (a real implementation would be more complex)
            cone = Part.makeCone(throat_radius, throat_radius * (1 + length / 100), length)
            obj.Shape = cone

    def create_horn():
        """Function called by a GUI Command to create a new horn object in the document."""
        doc = App.activeDocument()
        if doc is None:
            App.newDocument()
        obj = App.activeDocument().addObject("Part::FeaturePython", "Horn")
        Horn(obj) # Attach our Python class to the FreeCAD object
        obj.ViewObject.Proxy = 0 # Use the default view provider
        App.activeDocument().recompute()
    ```

-----

## 5\. Development & Testing Workflow

  * **Local Development:**
      * The primary development environment is FreeCAD itself. Use the **Python Console** and **Report View** for live coding and debugging.
      * For a better IDE experience, set up a Python environment (e.g., venv) and add the FreeCAD `bin` and `lib` paths to your `PYTHONPATH` to enable autocompletion in editors like VS Code.
      * To test the workbench, create a symbolic link from the FreeCAD `Mod/` directory to your git repository.
  * **Testing:**
      * **Unit Tests:** For pure-logic modules (e.g., acoustic calculations), use `pytest` to run tests outside of FreeCAD.
      * **Integration Tests:** Write Python scripts that can be executed by FreeCAD in headless mode (`freecadcmd -c <script.py>`). These scripts should create documents, add workbench objects, change parameters, and verify the results (e.g., check the resulting volume or run a basic FEM check).
  * **Debugging:**
      * Use `FreeCAD.Console.PrintMessage()` and `FreeCAD.Console.PrintError()` for logging.
      * Inspect object properties and the dependency graph in the GUI to troubleshoot recompute issues.
      * The FEM Workbench's solver output provides detailed logs for debugging simulation failures.

-----

## 6\. Specific Instructions for AI Collaboration

  * **Contribution Workflow (Pull Request Process):**
    1.  **Fork & Branch:** Create a feature branch from the `main` or `develop` branch.
    2.  **Implement:** Adhere to all coding conventions. Prioritize creating parametric, non-destructive tools.
    3.  **Document:** Add clear Python docstrings explaining classes and functions. Add comments for complex geometric or mathematical logic.
    4.  **Test:** If adding new logic, create or update a corresponding test script.
    5.  **Pull Request:** Submit a PR. The title should be prefixed with the relevant component, e.g., `[Waveguide] Add Tractrix flare calculation` or `[FEM] Improve acoustic mesh presets`. The PR description should explain the change and how to test it manually.
  * **Best Practices for AI:**
      * **Focus on Parametric Design:** When asked to generate geometry, always create a **Scripted Object** with properties. Do not generate simple shapes with hardcoded dimensions.
      * **Leverage Existing APIs:** Before writing complex geometric algorithms from scratch, check if a function in `Part` or a tool in `PartDesign` can do it more efficiently.
      * **Separate Logic and GUI:** Keep the core calculations and geometry creation logic separate from the `PySide` GUI code. The geometry modules should be usable from a script without any GUI interaction.
      * **Units:** FreeCAD is internally unitless (mm). When defining properties (`addProperty`), use `App::PropertyLength`, `App::PropertyFrequency`, etc., to allow the user to enter values with units (e.g., "1 inch", "1 kHz"). Always use the `.Value` attribute to get the internal float value in mm for calculations.