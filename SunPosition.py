import math

def GetSunPosition(DeltaGMT : float, NumberOfDays : int, Longitude : float, Latitude : float, LocalTime : float) -> tuple:
    # DeltaGMT is in hours
    # LocalTime is in hours
    LocalStandardTimeMeridian = 15 * DeltaGMT   # hours
    B = (360 / 365) * (NumberOfDays - 81)   # degrees
    EquationOfTime = 9.87 * math.sin(2 * math.radians(B)) - 7.53 * math.cos(math.radians(B)) - 1.5 * math.sin(math.radians(B))  # minutes
    TimeCorrection = 4 * (Longitude - LocalStandardTimeMeridian) + EquationOfTime   # minutes
    LocalSolarTime = LocalTime + TimeCorrection / 60    # hours
    HourAngle = 15 * (LocalSolarTime - 12)  # degrees
    Declanation = 23.45 * math.sin((math.radians(360/365)) * (NumberOfDays - 81))   # degrees
    Elevation = math.asin(math.sin(math.radians(Declanation)) * math.sin(math.radians(Latitude)) + math.cos(math.radians(Declanation)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(HourAngle)))  # radians
    Azimuth = math.acos(((math.sin(math.radians(Declanation)) * math.cos(math.radians(Latitude))) - (math.cos(math.radians(Declanation)) * math.sin(math.radians(Latitude)) * math.cos(math.radians(HourAngle)))) / math.cos(math.radians(Elevation)))  # radians
    return math.degrees(Elevation), math.degrees(Azimuth)

e, a = GetSunPosition(-7, 89, -118, 34, 17.5)

print(e)
print(a)

