

// Thickness of the stock to laser cut
stock_thickness = 2.3;

// Diameter of mounting holes
hole_diameter = 3;

// overhang of side panels beyond plates
side_allowance = 5;

pcb_frame_offset = 10;

keypad_plate_height = 20;
display_plate_height = 25;
display_angle = 25;

front_inset = 10;
back_inset = 10;
base_inset = 3;

display_back_distance = 130;

tab_length = 40;
tab_depth = stock_thickness;
tab_tolerance = .2;

keypad_width = 130;
keypad_height = 115;

display_height = 60;

display_dimensions = [90,35];

overall_footprint = [114.35 + 2*pcb_frame_offset, 180];

function display_top_coords() = [0,display_back_distance + cos(display_angle) * display_height,display_plate_height + sin(display_angle) * display_height];

module mounting_holes_2d(rows, columns, spacing, diameter) {
    for(row=[0:rows-1], col=[0:columns-1]) {
        translate([diameter/2,diameter/2,0])
        translate([(spacing.x+diameter)*col,(spacing.y+diameter)*row])    
        circle(d=diameter);
    }
}

module tabs2d(plate_dimensions, num_tabs, tab_length, end_spacing) {
    tab_spacing = (plate_dimensions.y - 2*end_spacing - num_tabs*tab_length)/(num_tabs-1);
    for(tab=[0:num_tabs-1]) {
        translate([-tab_depth, end_spacing + (tab_length+tab_spacing) * tab, 0])
        square([plate_dimensions.x+2*tab_depth, tab_length]);
    }
}

module keypad_plate() {
    // Measured from Adafruit NeoKey 5x6 Ortho Snap-Apart PCB
    pcb_dimensions = [114.35,115.55];
    
    mounting_hole_diameter = 2.90;
    mounting_hole_inset = [3.60,3.55]; // from PCB edge to hole edge
    mounting_hole_spacing = [101.20,102.50]; // between nearest hole edges
    
    keyswitch_inset = [2.65,12.20];
    
    // Preferences
    
    
    // Calculated
    frame_dimensions = [pcb_dimensions.x+pcb_frame_offset*2, pcb_dimensions.y+pcb_frame_offset*2];
    
    key_rows = 5;
    key_cols = 6;

    key_width = 14;
    key_height = key_width;

    module plate_frame(size) {
        translate([pcb_frame_offset,pcb_frame_offset,0])
        offset(delta=pcb_frame_offset)
        square(pcb_dimensions);
        // two tabs on each side
        tabs2d(frame_dimensions, 2, 45, 5);
    }

    module key_array(rows, columns, spacing) {
        for(row=[0:rows-1], col=[0:columns-1]) {
            translate([col * (key_width + spacing), 
                row * (key_width + spacing),0])
            square([key_width, key_height]);
        }
    }

    difference() {
        plate_frame([keypad_width, keypad_height]);
        
        translate([keyswitch_inset.x+pcb_frame_offset,
            keyswitch_inset.y+pcb_frame_offset,0])
        key_array(key_rows,key_cols,5.10);
        
        translate([mounting_hole_inset.x+pcb_frame_offset,
            mounting_hole_inset.y+pcb_frame_offset,0])
        mounting_holes_2d(2, 2, mounting_hole_spacing, hole_diameter);
    }
}

module display_plate() {
    // measured from LCD module
    screen_dimensions = [97.10, 39.65];
    pcb_dimensions = [98.25,59.90];
    mounting_hole_diameter = 3.45;
    hole_inset = [1.05,0.7];
    hole_spacing = [89.60, 51.50];
    display_inset = [0.6,10.05];
    
    display_tolerance = .5;
    offset_dimensions = [overall_footprint.x, pcb_dimensions.y+2*pcb_frame_offset];
    
    frame_x_offset = (overall_footprint.x - pcb_dimensions.x) / 2;
    
    module display_frame() {
        translate([-frame_x_offset, -pcb_frame_offset,0])square([overall_footprint.x, pcb_dimensions.y+2*pcb_frame_offset]);
        translate([-frame_x_offset,-pcb_frame_offset,0])
            tabs2d(offset_dimensions, 2, 20, 5);
    }
    
    module cutouts() {
        translate([display_inset.x, display_inset.y,0])offset(delta=display_tolerance)square(screen_dimensions);
        translate([hole_inset.x,hole_inset.y,0])mounting_holes_2d(2, 2, hole_spacing, mounting_hole_diameter);
    }

    translate([frame_x_offset,pcb_frame_offset,0])difference() {
        display_frame();
        cutouts();
    }
    
}

module base_plate(size) {
    square(size);
    tabs2d(size, 3, 40, 5);
}
 
module mounting_plates() {
    translate([tab_depth,0,0]){
        color("BurlyWood"){
            // Keypad Plate
            translate([0, front_inset, keypad_plate_height - stock_thickness])
                linear_extrude(stock_thickness)
                keypad_plate();
            
            // Display Plate
            translate([0,display_back_distance,display_plate_height])
                rotate([display_angle,0,0])
                translate([0,0,-stock_thickness])
                linear_extrude(stock_thickness)
                display_plate();
        }
        
        color("DimGray")
            // Base Plate
            translate([0, front_inset, 0])
            linear_extrude(stock_thickness)
            base_plate([keypad_width, overall_footprint.y - front_inset - back_inset]);
    }
}

module side_panel() {
    module slots2d() {
        offset(tab_tolerance)projection()intersection() {
            translate([0,0,-(overall_footprint.x + tab_depth + 1)])rotate([0,0,-90])rotate([0,-90,0])mounting_plates();
            cube([overall_footprint.y, display_top_coords().z, 2]);
        }
    }
    
    module side_polygon() {
        d2 = display_plate_height - (keypad_plate_height + side_allowance);
        d3 = side_allowance/cos(display_angle);
        x = (d2+d3)/tan(display_angle);
        hard_point_1 = [display_back_distance - x, keypad_plate_height + side_allowance];
        
        d4 = side_allowance / sin(display_angle);
        d5 = (side_allowance + d4) * tan(display_angle);
        y = display_top_coords().z + d5;
        hard_point_2 = [display_top_coords().y + side_allowance, y];

        offset(3)polygon([
        [front_inset - side_allowance, -base_inset],
        [front_inset - side_allowance,keypad_plate_height + side_allowance],
        hard_point_1,
        hard_point_2, 
        [overall_footprint.y,-base_inset]
        ]);
    }
    rotate([0,90,0])rotate([0,0,90])
    linear_extrude(stock_thickness)difference() {
        side_polygon();
        slots2d();
    }
}
*color("Sienna"){
    side_panel();
    translate([keypad_width+tab_depth,0,0])side_panel();
}
mounting_plates();
