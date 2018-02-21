## Code structure

```mermaid
graph TB
mat[Material] ==> target[Target]
geom[Geometry] ==> target
target[Target] ==> lpi[LaserPlasmaInteraction]
profile[Profile] ==> laser[Laser]
laser ==>lpi[LaserPlasmaInteraction]

lpi ==> pic[ParticleInCell]

input{user input} -x laser
input -x mat
input -x geom
input -x profile
```

## Estimations

```mermaid
graph LR
lpi[LaserPlasmaInteraction] --> plasma[PlasmaParameters]
lpi --> laser[Laser]
lpi --> target[Target]
lpi --> electron[Electron]
electron --> hot[Hot]
electron --> cold[Cold]
lpi --> ion[Ion]
lpi --> photon[Photon]
lpi --> positron[Positron]


hot -x outHot(Temperature, Energy cutoff, ...)
cold -x outCold(...)
ion -x outIon(Energy cutoff, ...)
photon -x outPhoton(...)
positron -x outPositron(...)
plasma -x outPlasma(Debye length, ...)
laser -x outLaser(Absorption efficiency, ...)
target -x outTarget(Spitzer conductivity, ...)
```

