
overall_dimensions = [130, 200, 60];
stock_thickness = 2.3;
hole_diameter = 3.75;

front_inset = 10;
back_inset = 10;
base_inset = 3;

keypad_plate_height = 30;
display_plate_height = 32;
display_back_distance = 130;

side_allowance = 5;

tab_length = 40;
tab_depth = stock_thickness;
tab_tolerance = .2;

keypad_width = 130;
keypad_height = 115;

display_height = 60;
display_angle = 30;
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
    translate([0,40,0])tab2d(size.x, size.y/2 - 20);
    translate([0,140,0])tab2d(size.x, size.y/2 - 20);
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
            translate([0,0,-(overall_dimensions.x + tab_depth + 1)])rotate([0,0,-90])rotate([0,-90,0])mounting_plates();
            cube([overall_dimensions.y, overall_dimensions.z, 2]);
        }
    }
    
    module side_polygon() {
        d2 = display_plate_height - (keypad_plate_height + side_allowance);
        d3 = side_allowance/cos(display_angle);
        x = d2+d3/tan(display_angle);
        hard_point_1 = [display_back_distance - x, keypad_plate_height + side_allowance];
        
        d4 = side_allowance / sin(display_angle);
        d5 = (side_allowance + d4) * tan(display_angle);
        y = display_top_coords().z + d5;
        hard_point_2 = [display_top_coords().y + side_allowance, y];

        polygon([
        [0,-base_inset],
        [10,keypad_plate_height + side_allowance],
        hard_point_1,
        hard_point_2, 
        [overall_dimensions.y,-base_inset]
        ]);
    }
    rotate([0,90,0])rotate([0,0,90])
    linear_extrude(stock_thickness)difference() {
        side_polygon();
        slots2d();
    }
}
color("Sienna"){
    side_panel();
    translate([keypad_width+tab_depth,0,0])side_panel();
}
mounting_plates();
