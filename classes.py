import pint  # for unit handling
from typing import Optional, List
from resources import bolt_sizes, materials, clearance_holes

# Load data at module level for efficiency
BOLT_SIZES = bolt_sizes()
MATERIALS = materials()
CLEARANCE_HOLES = clearance_holes()

# Initialize unit registry
u = pint.UnitRegistry()

class Bolt:
    """Represents a bolt with size, thread pitch, and material properties."""
    
    def __init__(self, size: str, tpi: str, material: str):
        tpi_key = str(tpi)  # normalize to string for dict key

        # Validate inputs early for clearer error messages
        if size not in BOLT_SIZES:
            raise ValueError(f"Bolt size {size} not available")
        if tpi_key not in BOLT_SIZES[size]['tpi']:
            raise ValueError(f"TPI {tpi} not available for bolt size {size}")
        if material not in MATERIALS:
            raise ValueError(f"Material {material} not available")

        self.size = size
        self.tpi = int(tpi_key)
        self.material = material

        # Load properties from database
        self.d = BOLT_SIZES[size]['d']
        self.A_t = BOLT_SIZES[size]['tpi'][tpi_key]['A_t']
        self.A_m = BOLT_SIZES[size]['tpi'][tpi_key]['A_m']

    def __repr__(self):
        return (f"Bolt(size='{self.size}', nominal_diameter={self.d:.3f}, "
                f"threads_per_inch={self.tpi}, tensile_stress_area={self.A_t:.4f}, "
                f"minor_diameter={self.A_m:.4f}, material='{self.material}')")
    
class Washer:
    """Represents a washer with dimensions and material."""
    
    def __init__(self, di: float, do: float, t: float, material: str = "carbon steel"):
        if di >= do:
            raise ValueError("Inner diameter must be less than outer diameter")
        if t <= 0:
            raise ValueError("Thickness must be positive")
            
        self.di = di
        self.do = do
        self.t = t
        self.material = material
    
    def __repr__(self):
        return (f"Washer(inner_diameter={self.di:.3f}, outer_diameter={self.do:.3f}, "
                f"thickness={self.t:.3f}, material='{self.material}')")

class Member:
    """Represents a structural member with thickness and material."""
    # ID Counter for unique identification
    _id_counter = 0

    def __init__(self, thickness: float, material: str = "steel"):
        if thickness <= 0:
            raise ValueError("Thickness must be positive")
        if material not in MATERIALS:
            raise ValueError(f"Material {material} not available")
            
        Member._id_counter += 1

        self.id = Member._id_counter
        self.thickness = thickness
        self.material = material
    
    def __repr__(self):
        return (f"Member(id={self.id}, thickness={self.thickness:.3f}, material='{self.material}')")
    
class BoltedJoint:
    """Represents a bolted joint consisting of a bolt, optional washers, and one or more members."""
    
    def __init__(self, bolt: Bolt, members: List[Member], clearance_hole: float, 
                 washers: Optional[List[Washer]] = None, preload: float = 0):
        if len(members) < 1:
            raise ValueError("At least one member is required")
        if clearance_hole <= bolt.d:
            raise ValueError("Clearance hole must be larger than bolt diameter")
        if preload < 0:
            raise ValueError("Preload cannot be negative")
            
        self.bolt = bolt
        self.members = members
        self.washers = washers if washers is not None else []
        self.clearance_hole = clearance_hole
        self.preload = preload
    
    def __repr__(self):
        return (f"BoltedJoint(bolt={self.bolt.size}, members_count={len(self.members)}, "
                f"clearance_hole={self.clearance_hole:.3f}, preload={self.preload})")

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
        if self.bolt.material not in MATERIALS:
            raise ValueError(f"Material {self.bolt.material} not found in materials database")
        
        E_bolt = MATERIALS[self.bolt.material]['E']  # Elastic modulus in Pa
        A_t = self.bolt.A_t  # Tensile stress area in in²
        L_grip = self.grip_length()  # Grip length in inches
        
        # Convert area from in² to m²
        A_t_m2 = A_t * 0.00064516  # 1 in² = 0.00064516 m²
        L_grip_m = L_grip * 0.0254  # 1 inch = 0.0254 meters
        
        # Bolt stiffness k_b = (E * A) / L
        k_bolt = (E_bolt * A_t_m2) / L_grip_m  # N/m
        
        return k_bolt
