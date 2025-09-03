import pint # for unit handling
from typing import Optional
from resources import bolt_sizes, materials, clearance_holes

BOLT_SIZES = bolt_sizes()
MATERIALS = materials()
CLEARANCE_HOLES = clearance_holes()

u = pint.UnitRegistry()

class Bolt:
    def __init__(self, size, tpi, material):
        tpi_key = str(tpi)  # normalize to string for dict key

        # Optional: validate early for clearer error messages
        if tpi_key not in BOLT_SIZES[size]['tpi']:
            raise ValueError(f"TPI {tpi} not available for bolt size {size}")

        self.size = size
        self.tpi = int(tpi_key)  # or keep as string if you prefer
        self.material = material

        self.d   = BOLT_SIZES[size]['d']
        self.A_t = BOLT_SIZES[size]['tpi'][tpi_key]['A_t']
        self.A_m = BOLT_SIZES[size]['tpi'][tpi_key]['A_m']

    def __repr__(self):
        return (f"Bolt(size={self.size}, nominal_diameter={self.d},"
                f"threads_per_inch={self.tpi}, tensile_stress_area={self.A_t}"
                f"minor_diameter={self.A_m}, material={self.material})")
    
class Washer: 
    def __init__(self, di, do, t, material="carbon steel"):
        self.di = di
        self.do = do
        self.t = t
        self.material = material
    
    def __repr__(self):
        return (f"Washer(inner_diameter={self.di}, outer_diameter={self.do}, thickness={self.t})")

class Member:
    # ID Counter
    _id_counter = 0

    def __init__(self, thickness, material="steel"):
        Member._id_counter += 1

        self.id = Member._id_counter
        self.thickness = thickness
        self.material = material
    
    def __repr__(self):
        return (f"Member(name={self.id}, thickness={self.thickness}, material={self.material})")
    
class BoltedJoint:
    def __init__(self, bolt: Bolt, members: list[Member], clearance_hole: float, washers: Optional[list[Washer]] = None, preload: float = 0):
        """A bolted joint consisting of a bolt, optional washers, and one or more members."""
        self.bolt = bolt
        self.members = members
        self.washers = washers if washers is not None else []
        self.clearance_hole = clearance_hole
        self.preload = preload
    
    def __repr__(self):
        return (f"BoltedJoint(bolt={self.bolt}, members={self.members}, washers={self.washers})")

    def grip_length(self):
        """Calculate the total grip length of the bolted joint."""
        total_t = sum(member.thickness for member in self.members)
        if self.washers:
            for washer in self.washers:
                total_t += washer.t
        return total_t
    
    def apply_preload(self, preload):
        """Apply a preload to the bolted joint."""
        self.preload = preload

    def apply_loads(self, axial_load: float, shear_load: float = 0):
        """Apply an axial load to the bolted joint."""
        self.axial_load = axial_load
        self.shear_load = shear_load
    
    def remove_loads(self, axial_load: float = 0, shear_load: float = 0):
        """Remove applied loads from the bolted joint."""
        self.axial_load = axial_load
        self.shear_load = shear_load

    def bolt_stiffness(self):
        """Calculate the stiffness of the bolt from the grip and shank length."""

