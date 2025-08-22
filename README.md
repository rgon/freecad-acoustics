# FreeCAD Acoustics
[WIP] a collection of tools to design advanced loudspeakers with Open Source Software. It will run inside FreeCAD as a workbench, thanks to its expandability.

> Looking for help!
> This is not a project with an expected deadline, but rather a compilation of tools that will be useful in loudspeaker design.
> Creating a collection of Open Source software for these purposes will allow PROPER 'hobby' design, taking less time while learning more.
> Heck, maybe next time you go out for dinner you won't leave early because the system sounds like a goose.
> It is my way to contribute to the audio community of which I've learned a lot.

----------------------

# TODO
## Stage 0: Boilerplate
+ [x] Concept definition: create some kind of parametric waveguide script
+ [ ] Implement as freeCAD workbench / easy updating / CICD -> don't require copying and pasting a macro. NOTE: modify the .ai/INSTRUCTIONS.md file with any relevant CICD changes.

## Stage 1: Waveguide definition
Because being in the ballpark is not the same as being mathematically correct.

**GOAL:**
+ [ ] Tom Danley's Paraline profile (what we started with)
    + [ ] With XY pathlength offset
+ [ ] OS waveguide profile
+ [ ] Equalized pathlength asymmetric waveguide (Charles Sprinkle's Image Control)
+ [ ] Metacomponent to add width to the waveguide profile, add a flange etc.

## Stage 2: Simulation (ATH, but FOSS)

**GOAL:**
+ [ ] Be able to model a simple waveguide https://youtu.be/NzAnPgw_Dic?si=-HpwaKmyuil5wxTZ&t=2015

**Options:**
NOTE: once we get into reading arxiv papers, it's probably too involved for the scope/resources I can dedicate to this.

### 1st: Meshing - Export mesh to external solver
+ Export to Marcel Batik's ATH (not Open source, we cannot integrate :/) or ABEC.
+ Approximate export to hornresp for quick measurements?

### BEM, like ABEC
+ FOSS BEM Meshing & export https://arxiv.org/abs/2312.00005
+ http://www.openbem.dk/
+ https://bempp.com/
+ Does a GPU Solver exist? https://digibug.ugr.es/handle/10481/97162?show=full

### FEM Acoustics simulation
+ Are FR responses Possible in CalculiX? https://forum.freecad.org/viewtopic.php?t=93242
+ GPU Solver exists for FEM? https://www.sciencedirect.com/science/article/abs/pii/S016926072300281X https://www.sciencedirect.com/science/article/abs/pii/S0010465523001479 https://github.com/ribesstefano/GPU-accelerated-Finite-Element-Method-using-Python-and-CUDA

## Stage 3: Physical simulation
Because FreeCAD can already do FEM mechanical simulations! (see box resonance, vibration modes...) https://www.facebook.com/groups/736353126390291/posts/29469495112649376/