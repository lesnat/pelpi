```mermaid
graph TB
prof[Profile] ==> las[Laser]
in{User input} -x prof
in{User input} -x las

prof --> timeIntegral
prof --> spaceIntegralDouble

las --> intensity(intensity)
las --> intensityNormalized(intensityNormalized)
```

