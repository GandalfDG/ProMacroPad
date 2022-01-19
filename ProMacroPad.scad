use <BOSL/transforms.scad>
include <NopSCADlib/core.scad>
include <NopSCADlib/vitamins/pcbs.scad>

overall_dimensions = [130, 200, 60];
stock_thickness = 2.3;
hole_diameter = 3.75;

front_inset = 10;
back_inset = 10;
base_inset = 3;

keypad_plate_height = 30;
display_plate_height = 35;
display_back_distance = 130;

side_allowance = 8;

tab_length = 40;
tab_depth = stock_thickness;
tab_tolerance = .2;

keypad_width = 130;
keypad_height = 115;

display_height = 60;
display_angle = 40;
display_dimensions = [90,35];

function display_top_coords() = [0,display_back_distance + cos(display_angle) * display_height,display_plate_height + sin(display_angle) * display_height];

module mounting_holes_2d(rows, columns, spacing) {
    for(row=[0:rows-1], col=[0:columns-1]) {
        translate([col * spacing.x, row * spacing.y])
            circle(hole_diameter);
    }
}

module tab2d(plate_width, length) {
    translate([plate_width/2,0])square([plate_width+2*tab_depth, length],center=true);
}

module keypad_plate() {
    key_rows = 5;
    key_cols = 6;

    key_width = 14;
    key_height = key_width;

    mounting_hole_spacing = [110, 105];

    module plate_frame(size) {
        square([size.x,size.y]);
        // two tabs on each side
        translate([size.x/2,90])square([size.x + 2*tab_depth, tab_length],center=true);
        translate([size.x/2,30])square([size.x + 2*tab_depth, tab_length],center=true);
    }

    module key_array(rows, columns, spacing) {
        for(row=[0:rows-1], col=[0:columns-1]) {
            translate([col * (key_width + spacing), row * (key_width + spacing),0])
                square([key_width, key_height]);
        }
    }

    difference() {
        plate_frame([keypad_width,120]);
        translate([10,15])key_array(key_rows,key_cols,5);
        translate([10,8])mounting_holes_2d(2, 2, mounting_hole_spacing);
    }
}

module display_plate(size) {
    module display_frame(size) {
        square(size);
        translate([0,size.y/2])tab2d(size.x, size.y - 10);
    }

    difference() {
        display_frame([size.x,size.y]);
        translate([size.x/2,size.y/2])square(display_dimensions, center=true);
        translate([10, 20])mounting_holes_2d(2, 2, [105, 30]);
    }
    
}

module base_plate(size) {
    square(size);
    back(40)tab2d(size.x, size.y/2 - 20);
    back(140)tab2d(size.x, size.y/2 - 20);
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
                down(stock_thickness)
                linear_extrude(stock_thickness)
                display_plate([keypad_width, display_height]);
        }
        
        color("DimGray")
            // Base Plate
            translate([0, front_inset, 0])
            linear_extrude(stock_thickness)
            base_plate([keypad_width, overall_dimensions.y - front_inset - back_inset]);
    }
}

module side_panel() {
    module slots2d() {
        offset(tab_tolerance)projection()intersection() {
            down(overall_dimensions.x + tab_depth + 1)zrot(-90)yrot(-90)mounting_plates();
            cube([overall_dimensions.y, overall_dimensions.z, 2]);
        }
    }
    
    module side_polygon() {
        function difficult_point() = 
            1/tan(display_angle) * (display_plate_height - keypad_plate_height) 
            + (1/cos(display_angle) * side_allowance);
        function back_corner_x() = display_top_coords().y + side_allowance;
        function back_corner_y() = tan(display_angle) * (side_allowance + (1/tan(display_angle) * side_allowance)) + display_top_coords().z;
        polygon([
        [0,-base_inset],
        [10,keypad_plate_height + side_allowance],
        [display_back_distance - difficult_point(), keypad_plate_height + side_allowance],
        [back_corner_x(), back_corner_y()], 
        [overall_dimensions.y,-base_inset]
        ]);
    }
    yrot(90)zrot(90)
    linear_extrude(stock_thickness)difference() {
        side_polygon();
        slots2d();
    }
}
color("Sienna"){
    side_panel();
    right(keypad_width+tab_depth)side_panel();
}
mounting_plates();
translate([keypad_width/2 + tab_depth,overall_dimensions.y - 30,stock_thickness + 1])zrot(180)pcb(RPI0);

