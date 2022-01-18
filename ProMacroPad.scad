use <BOSL/transforms.scad>
include <NopSCADlib/core.scad>
include <NopSCADlib/vitamins/pcbs.scad>

stock_thickness = 2.3;
through_thickness = stock_thickness + 10;

hole_diameter = 3.75;

tab_length = 40;
tab_depth = stock_thickness;
tab_tolerance = .2;

keypad_width = 130;
keypad_height = 115;

display_height = 60;
display_angle = 25;
display_dimensions = [90,35];

module mounting_holes(rows, columns, spacing) {
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
        translate([10,8])mounting_holes(2, 2, mounting_hole_spacing);
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
        translate([10, 20])mounting_holes(2, 2, [105, 30]);
    }
    
}

module base_plate(size) {
    square(size);
    back(40)tab2d(size.x, size.y/2 - 20);
    back(140)tab2d(size.x, size.y/2 - 20);
}
 
module mounting_plates() {
    translate([tab_depth,0,20]){
        color("BurlyWood"){
        linear_extrude(stock_thickness)keypad_plate();
        translate([0,120,10])rotate([display_angle,0,0])linear_extrude(stock_thickness)display_plate([keypad_width, display_height]);
        
        }
        color("DarkGray")down(20)linear_extrude(stock_thickness)base_plate([keypad_width, 180]);
    }
}

module side_panel() {
    module slots2d() {
        offset(tab_tolerance)projection()intersection() {
            back(5)up(tab_depth - .5)right(180)zrot(90)yrot(90)mounting_plates();
            cube([180, 180, 2]);
        }
    }

    linear_extrude(stock_thickness)difference() {
        offset(10)hull()slots2d();
        slots2d();
    }
}


color("Sienna")right(tab_depth)back(180)rotate([90,0,-90])side_panel();
color("Sienna")right(tab_depth + keypad_width + stock_thickness)back(180)rotate([90,0,-90])side_panel();
up(5)mounting_plates();
translate([keypad_width/2 + tab_depth,150,10])zrot(180)pcb(RPI0);

