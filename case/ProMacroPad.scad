// Thickness of the stock to laser cut
stock_thickness = 2.3;

keypad_plate_height = 20;
display_plate_height = keypad_plate_height + 10;
display_angle = 20;
display_back_distance = 135;

tab_depth = stock_thickness;
tab_tolerance = .2;


// keypad measurements
// Measured from Adafruit NeoKey 5x6 Ortho Snap-Apart PCB
keypad_pcb_dimensions = [114.35, 115.55];

keypad_mounting_hole_diameter = 2.90;
keypad_mounting_hole_inset = [3.60, 3.55]; // from PCB edge to hole edge
keypad_mounting_hole_spacing = [101.20, 102.50]; // between nearest hole edges

keyswitch_inset = [2.65, 12.20];
keyswitch_spacing = 5.05;


// display measurements
// measured from LCD module
display_screen_dimensions = [97.10, 39.65];
display_pcb_dimensions = [98.25, 59.90];
display_mounting_hole_diameter = 3.45;
display_hole_inset = [1.05, 0.7];
display_hole_spacing = [89.60, 51.50];
display_inset = [0.6, 10.05];


// overhang of side panels beyond plates
side_panel_offset = 5;

pcb_frame_offset = 10;

// calculated properties
keypad_frame_dimensions = [keypad_pcb_dimensions.x + 2*pcb_frame_offset,keypad_pcb_dimensions.y + 2*pcb_frame_offset];
display_frame_height = display_pcb_dimensions.y + 2*pcb_frame_offset;
function display_top_coords() = [0,display_back_distance + cos(display_angle) * display_frame_height,display_plate_height + sin(display_angle) * display_frame_height];

// FIXME
overall_footprint = [keypad_frame_dimensions.x, display_top_coords().y];


module mounting_holes_2d(rows, columns, spacing, diameter) {
    for(row=[0:rows-1], col=[0:columns-1]) {
        translate([diameter/2,diameter/2,0])
        translate([(spacing.x+diameter)*col,(spacing.y+diameter)*row])    
        circle(d=diameter, $fs=.3);
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
    
    // Calculated
    frame_dimensions = [keypad_pcb_dimensions.x+pcb_frame_offset*2, keypad_pcb_dimensions.y+pcb_frame_offset*2];
    
    key_rows = 5;
    key_cols = 6;

    key_width = 14;
    key_height = key_width;

    module plate_frame() {
        translate([pcb_frame_offset,pcb_frame_offset,0])
        offset(delta=pcb_frame_offset)
        square(keypad_pcb_dimensions);
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
        plate_frame();
        
        translate([keyswitch_inset.x+pcb_frame_offset,
            keyswitch_inset.y+pcb_frame_offset,0])
        key_array(key_rows,key_cols,keyswitch_spacing);
        
        translate([keypad_mounting_hole_inset.x+pcb_frame_offset,
            keypad_mounting_hole_inset.y+pcb_frame_offset,0])
        mounting_holes_2d(2, 2, keypad_mounting_hole_spacing, keypad_mounting_hole_diameter);
    }
}

module display_plate() {
    // measured from LCD module
    
    display_tolerance = .5;
    offset_dimensions = [overall_footprint.x, display_pcb_dimensions.y+2*pcb_frame_offset];
    
    frame_x_offset = (overall_footprint.x - display_pcb_dimensions.x) / 2;
    
    module display_frame() {
        translate([-frame_x_offset, -pcb_frame_offset,0])square([overall_footprint.x, display_pcb_dimensions.y+2*pcb_frame_offset]);
        translate([-frame_x_offset,-pcb_frame_offset,0])
            tabs2d(offset_dimensions, 2, 25, 5);
    }
    
    module cutouts() {
        offset(delta=display_tolerance)
        translate([display_inset.x, display_inset.y,0])square(display_screen_dimensions);
        translate([display_hole_inset.x,display_hole_inset.y,0])
        mounting_holes_2d(2, 2, display_hole_spacing, display_mounting_hole_diameter);
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
            translate([0, 0, keypad_plate_height - stock_thickness])
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
            translate([0, 0, 0])
            linear_extrude(stock_thickness)
            base_plate([overall_footprint.x, overall_footprint.y]);
    }
}

module side_panel() {
    module slots2d() {
        offset(tab_tolerance)projection()intersection() {
            translate([0,0,-(overall_footprint.x + tab_depth + 1)])rotate([0,0,-90])rotate([0,-90,0])mounting_plates();
            // FIXME
            cube([overall_footprint.y + 30, display_top_coords().z + 20, 2]);
        }
    }
    
    module side_polygon() {
        d2 = display_plate_height - (keypad_plate_height + side_panel_offset);
        d3 = side_panel_offset/cos(display_angle);
        x = (d2+d3)/tan(display_angle);
        hard_point_1 = [display_back_distance - x, keypad_plate_height + side_panel_offset];
        
        d4 = side_panel_offset / sin(display_angle);
        d5 = (side_panel_offset + d4) * tan(display_angle);
        y = display_top_coords().z + d5;
        hard_point_2 = [display_top_coords().y + side_panel_offset, y];

        offset(3)polygon([
        [- side_panel_offset, 0],
        [- side_panel_offset,keypad_plate_height + side_panel_offset],
        hard_point_1,
        hard_point_2, 
        [overall_footprint.y+side_panel_offset,0]
        ]);
    }
    difference() {
        side_polygon();
        slots2d();
    }
}
module pieces_2d() {
    keypad_plate();
    translate([0, keypad_frame_dimensions.y + 10,0])display_plate();
    translate([overall_footprint.x + 10, 0,0])base_plate(overall_footprint);
    translate([overall_footprint.x * 2 + 30,0,0])side_panel();
    translate([overall_footprint.x * 2 + 30,100,0])side_panel();
}

pieces_2d();

//*mounting_plates();
//*color("Sienna"){
//    side_panel();
//    translate([overall_footprint.x+tab_depth,0,0])side_panel();
//}