import rhinoscriptsyntax as rs

import Rhino

def table_maker(width, depth, height, stock, tolerance, radius, router_bit):
    
    if stock > router_bit + tolerance and radius < 1.5 and stock < 3.5:
   
        #Create Table Top and Table Locations
       
        move_over = (width, 0, 0)
        move_over_again = (width * 2 + 2, 0, 0)
       
        table_top = rs.AddRectangle(rs.WorldXYPlane(), width, depth)
        rs.AddPoint(2 + stock, 2 + (stock - 0.05), 0)
        offset_x = 2.5
        offset_y = 2.5
        lst_x = [offset_x, width - offset_x, offset_x, width - offset_x]
        lst_y = [offset_y, offset_y, depth - offset_y, depth - offset_y]
        
        rs.MoveObjects(table_top, move_over_again)
       
        #Delete Reference Point
       
        rs.ObjectsByType(1, True)
        rs.Command("_Delete")
       
        #Create Tabs
       
        for i in range(0, 4):
           
            #Tab Dimensions
           
            tab_width = 2 + tolerance
            tab_height = stock + tolerance
           
            #Append Tab Locations
           
            tabs = rs.AddRectangle((lst_x[i], lst_y[i], 0), tab_width, tab_height)
            
            tp1 = rs.AddPoint(-tab_width/2, -tab_height/2, 0)
            tp2 = rs.AddPoint(tab_width/2, -tab_height/2, 0)
            tp3 = rs.AddPoint(-tab_width/2, tab_height/2, 0)
            tp4 = rs.AddPoint(tab_width/2, tab_height/2, 0)
            
            tab_point_group = [tp1, tp2, tp3, tp4]
            
            tabs_and_pts = [tabs]
            print(rs.MoveObject(tabs_and_pts, ( (-tab_width/2), (-tab_height/2), 0)))
            rs.MoveObjects(tabs_and_pts, move_over_again)
           
        #Leg 01
        
        leg_01_fillet_x = [radius, width - radius, radius, width - radius] 
        leg_01_fillet_y = [radius, radius, height - radius, height - radius]
        leg_01_z_rotations = [180, -90, 90, 0]
        
        
        leg_01_outer_fillets = []
        for i in range(0, 4):
            outer_fillets_not_rotated = rs.AddArc((leg_01_fillet_x[i], leg_01_fillet_y[i], 0), radius, 90)
            leg_01_outer_fillets.append(rs.RotateObject(outer_fillets_not_rotated, (leg_01_fillet_x[i], leg_01_fillet_y[i], 0), leg_01_z_rotations[i]))
            
        
        slot_line_01 = rs.AddLine((0, radius, 0), (0, ((height / 2) - 0.0525), 0))
        slot_line_02 = rs.AddLine((0, radius, 0), (0, ((height / 2) - 0.0525), 0))
        
        rs.MoveObject(slot_line_01, ((5 - (stock + tolerance))/2, 0, 0))
        rs.MoveObject(slot_line_02, ((5 - (stock + tolerance))/2 + stock + tolerance, 0, 0))
        
        arc_x_1 = (5 - (stock + tolerance)) / 2 + (router_bit / 2)
        arc_y_1 = (height / 2) - 0.0525
        arc_1_center = (arc_x_1, arc_y_1, 0)
        arc_x_2 = (5 - (stock + tolerance))/2 + stock + tolerance - (router_bit /2)
        arc_y_2 = (height / 2) - 0.0525
        arc_2_center = (arc_x_2, arc_y_2, 0)
        
        slot_fillet_1 = rs.RotateObject(rs.AddArc(arc_1_center, router_bit / 2, 90), arc_1_center, 90)
        slot_fillet_2 = rs.RotateObject(rs.AddArc(arc_2_center, router_bit / 2, 90), arc_2_center, 0)
        slot_fillet_3 = rs.RotateObject(rs.AddArc((2.5 - (stock/2) - (tolerance/2) - radius, radius, 0), radius, 90), (2.5 - (stock/2) - (tolerance/2) - radius, radius, 0), -90)
        slot_fillet_4 = rs.RotateObject((rs.AddArc((2.5 + (tolerance/2) + (stock/2) + radius, radius, 0), radius, 90)), (2.5 + (tolerance/2) + (stock/2) + radius, radius, 0), 180)
        leg_tab = rs.AddPolyline([(1.5, height, 0), (1.5, height + stock, 0), (3.5, height + stock, 0), (3.5, height, 0)])
        apex = rs.AddLine((arc_x_1, arc_y_1 + (router_bit/2), 0), (arc_x_2, arc_y_2 + (router_bit/2), 0))
        slot_fillets_and_tab = [slot_fillet_1, slot_fillet_2, slot_fillet_3, slot_fillet_4, slot_line_01, slot_line_02, leg_tab, apex]
        slot_fillets_and_tab_mirror = rs.MirrorObjects(slot_fillets_and_tab, (width / 2, 0, 0), (width / 2, 1, 0), copy = True)
        
        leg_01_perimeter1 = rs.AddLine((0, radius, 0), (0, height - radius, 0))
        leg_01_perimeter2 = rs.AddLine((radius, height, 0), (1.5, height, 0))
        leg_01_perimeter3 = rs.AddLine((3.5, height, 0), (width - 3.5, height, 0))
        leg_01_perimeter4 = rs.AddLine((width - 1.5, height, 0), (width - radius, height, 0))
        leg_01_perimeter5 = rs.AddLine((width, height - radius, 0), (width, radius, 0))
        leg_01_perimeter6 = rs.AddLine((width - radius, 0, 0), ((width - 2.5 + radius + (stock/2) + (tolerance/2), 0, 0)))
        leg_01_perimeter7 = rs.AddLine((width - 2.5 - radius - (stock/2) - (tolerance/2), 0, 0), (2.5 + (stock/2) + (tolerance/2) + radius, 0, 0)) 
        leg_01_perimeter8 = rs.AddLine((2.5 - (stock/2) - (tolerance/2) - radius, 0, 0), (radius, 0, 0))
        
        leg_01_curves = [slot_fillets_and_tab, slot_fillets_and_tab_mirror,
        leg_01_perimeter1, leg_01_perimeter2, leg_01_perimeter3, leg_01_perimeter4, leg_01_perimeter5, leg_01_perimeter6, leg_01_perimeter7, leg_01_perimeter8, 
        leg_01_outer_fillets]
        
        leg_01_list = []
        for sublist in leg_01_curves:
            if type(sublist) == type(slot_fillet_3):
                leg_01_list.append(sublist)
            elif type(sublist) == type(slot_fillets_and_tab):
                for curve in sublist:
                    leg_01_list.append(curve)
                    
                    
        tab_point_1 = rs.AddPoint((1.5, height + (router_bit/2), 0))
        tab_point_2 = rs.AddPoint((3.5, height + (router_bit/2), 0))
        tab_point_3 = rs.AddPoint((width - 3.5, height + (router_bit/2), 0))
        tab_point_4 = rs.AddPoint((width - 1.5, height + (router_bit/2), 0))
        
        tab_points = [tab_point_1, tab_point_2, tab_point_3, tab_point_4]
        
        leg_01 = rs.JoinCurves(leg_01_list)
        
        rs.MoveObject(leg_01, move_over)
        rs.MoveObjects(tab_points, move_over)
        
        #Leg_01 Inside
        
        if width > 10 + radius + radius + tolerance:
            infil_01 = rs.RotateObject((rs.AddArc((5 + radius, 3.25 + radius, 0), radius, 90)), (5 + radius, 3.25 + radius, 0), 180)
            infil_02 = rs.RotateObject((rs.AddArc((width - 5 - radius, 3.25 + radius, 0), radius, 90)), (width - 5 - radius, 3.25 + radius, 0), -90)
            infil_03 = rs.RotateObject((rs.AddArc((5 + radius, height - 3.25 - radius, 0), radius, 90)), (5 + radius, height - 3.25 - radius, 0), 90)
            infil_04 = rs.AddArc((width - 5 - radius, height - 3.25 - radius, 0), radius, 90)
            inperim_01 = rs.AddLine((5 + radius, 3.25, 0), (width - 5 - radius, 3.25, 0))
            inperim_02 = rs.AddLine((5, 3.25 + radius, 0), (5, height - 3.25 - radius, 0))
            inperim_03 = rs.AddLine((5 + radius, height - 3.25, 0), (width - 5 - radius, height - 3.25, 0))
            inperim_04 = rs.AddLine((width - 5, height - 3.25 - radius, 0), (width - 5, 3.25 + radius, 0))
            
            leg_01_inner_curves = [infil_01, infil_02, infil_03, infil_04, inperim_01, inperim_02, inperim_03, inperim_04]
            
            leg_01_inner = rs.JoinCurves(leg_01_inner_curves)
            
            rs.MoveObject(leg_01_inner, move_over)
            
         
            #Leg 02
        
        leg_02_fillet_x = [radius, depth - radius, radius, depth - radius] 
        leg_02_fillet_y = [radius, radius, height - radius, height - radius]
        leg_02_z_rotations = [180, -90, 90, 0]
        
        
        leg_02_outer_fillets = []
        for i in range(0, 4):
            t2outer_fillets_not_rotated = rs.AddArc((leg_02_fillet_x[i], leg_02_fillet_y[i], 0), radius, 90)
            leg_02_outer_fillets.append(rs.RotateObject(t2outer_fillets_not_rotated, (leg_02_fillet_x[i], leg_02_fillet_y[i], 0), leg_02_z_rotations[i]))
            
        
        t2slot_line_01 = rs.AddLine((0, radius, 0), (0, ((height / 2) - 0.0525), 0))
        t2slot_line_02 = rs.AddLine((0, radius, 0), (0, ((height / 2) - 0.0525), 0))
        
        rs.MoveObject(t2slot_line_01, ((5 - (stock + tolerance))/2, 0, 0))
        rs.MoveObject(t2slot_line_02, ((5 - (stock + tolerance))/2 + stock + tolerance, 0, 0))
        
        t2arc_x_1 = (5 - (stock + tolerance)) / 2 + (router_bit / 2)
        t2arc_y_1 = (height / 2) - 0.0525
        t2arc_1_center = (t2arc_x_1, t2arc_y_1, 0)
        t2arc_x_2 = (5 - (stock + tolerance))/2 + stock + tolerance - (router_bit /2)
        t2arc_y_2 = (height / 2) - 0.0525
        t2arc_2_center = (t2arc_x_2, t2arc_y_2, 0)
        
        t2slot_fillet_1 = rs.RotateObject(rs.AddArc(t2arc_1_center, router_bit / 2, 90), t2arc_1_center, 90)
        t2slot_fillet_2 = rs.RotateObject(rs.AddArc(t2arc_2_center, router_bit / 2, 90), t2arc_2_center, 0)
        t2slot_fillet_3 = rs.RotateObject(rs.AddArc((2.5 - (stock/2) - (tolerance/2) - radius, radius, 0), radius, 90), (2.5 - (stock/2) - (tolerance/2) - radius, radius, 0), -90)
        t2slot_fillet_4 = rs.RotateObject((rs.AddArc((2.5 + (tolerance/2) + (stock/2) + radius, radius, 0), radius, 90)), (2.5 + (tolerance/2) + (stock/2) + radius, radius, 0), 180)
        t2apex = rs.AddLine((t2arc_x_1, t2arc_y_1 + (router_bit/2), 0), (t2arc_x_2, t2arc_y_2 + (router_bit/2), 0))
        t2slot_fillets_and_tab = [t2slot_fillet_1, t2slot_fillet_2, t2slot_fillet_3, t2slot_fillet_4, t2slot_line_01, t2slot_line_02, t2apex]
        t2slot_fillets_and_tab_mirror = rs.MirrorObjects(t2slot_fillets_and_tab, (depth / 2, 0, 0), (depth / 2, 1, 0), copy = True)
        
        leg_02_perimeter1 = rs.AddLine((0, radius, 0), (0, height - radius, 0))
        leg_02_perimeter2 = rs.AddLine((radius, height, 0), (depth - radius, height, 0))
        leg_02_perimeter5 = rs.AddLine((depth, height - radius, 0), (depth, radius, 0))
        leg_02_perimeter6 = rs.AddLine((depth - radius, 0, 0), ((depth - 2.5 + radius + (stock/2) + (tolerance/2), 0, 0)))
        leg_02_perimeter7 = rs.AddLine((depth - 2.5 - radius - (stock/2) - (tolerance/2), 0, 0), (2.5 + (stock/2) + (tolerance/2) + radius, 0, 0)) 
        leg_02_perimeter8 = rs.AddLine((2.5 - (stock/2) - (tolerance/2) - radius, 0, 0), (radius, 0, 0))
        
        leg_02_curves = [t2slot_fillets_and_tab, t2slot_fillets_and_tab_mirror,
        leg_02_perimeter1, leg_02_perimeter2, leg_02_perimeter5, leg_02_perimeter6, leg_02_perimeter7, leg_02_perimeter8, 
        leg_02_outer_fillets]
        
        leg_02_list = []
        for sublist in leg_02_curves:
            if type(sublist) == type(t2slot_fillet_3):
                leg_02_list.append(sublist)
            elif type(sublist) == type(t2slot_fillets_and_tab):
                for curve in sublist:
                    leg_02_list.append(curve)
                    
                    
        
        leg_02 = rs.JoinCurves(leg_02_list)
        
        
        #Leg_02 Inside
        
        if depth > 10 + radius + radius + tolerance:
            t2infil_01 = rs.RotateObject((rs.AddArc((5 + radius, 3.25 + radius, 0), radius, 90)), (5 + radius, 3.25 + radius, 0), 180)
            t2infil_02 = rs.RotateObject((rs.AddArc((depth - 5 - radius, 3.25 + radius, 0), radius, 90)), (depth - 5 - radius, 3.25 + radius, 0), -90)
            t2infil_03 = rs.RotateObject((rs.AddArc((5 + radius, height - 3.25 - radius, 0), radius, 90)), (5 + radius, height - 3.25 - radius, 0), 90)
            t2infil_04 = rs.AddArc((depth - 5 - radius, height - 3.25 - radius, 0), radius, 90)
            t2inperim_01 = rs.AddLine((5 + radius, 3.25, 0), (depth - 5 - radius, 3.25, 0))
            t2inperim_02 = rs.AddLine((5, 3.25 + radius, 0), (5, height - 3.25 - radius, 0))
            t2inperim_03 = rs.AddLine((5 + radius, height - 3.25, 0), (depth - 5 - radius, height - 3.25, 0))
            t2inperim_04 = rs.AddLine((depth - 5, height - 3.25 - radius, 0), (depth - 5, 3.25 + radius, 0))
            
            leg_02_inner_curves = [t2infil_01, t2infil_02, t2infil_03, t2infil_04, t2inperim_01, t2inperim_02, t2inperim_03, t2inperim_04]
            
            leg_02_inner = rs.JoinCurves(leg_02_inner_curves)
         
        rs.Command("SelOpenCrv")
        rs.Command("Delete")
    
    else:
        print "WARNING: Stock Thickness Cannot Be Larger Than Router Bit and must be less than 3 inches, Fillet Radius Cannot Be Larger Than 1.5"
    
    
table_maker(24, 84, 12, .75, 0.02, 0.5, 0.375)

#KEY

    #first number = table width

    #second number = table depth

    #third number = table height

    #fourth number = stock thickness

    #fifth number = tolerance

    #sixth number = fillet radius

    #seventh number = router bit diameter

