import rhinoscriptsyntax as rs

import Rhino

def table_maker(width, depth, height, stock, tolerance, radius):
   
    #Create Table Top and Table Locations
   
    move_over = (width + 2, 0, 0)
   
    table_top = rs.AddRectangle(rs.WorldXYPlane(), width, depth)
    rs.AddPoint(2 + stock, 2 + (stock - 0.05), 0)
    offset_x = 2.5
    offset_y = 2.45
    lst_x = [offset_x, width - offset_x, offset_x, width - offset_x]
    lst_y = [offset_y, offset_y, depth - offset_y, depth - offset_y]
    
    rs.MoveObjects(table_top, move_over)
   
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
        print(rs.MoveObject(tabs, ( (-tab_width/2), (-tab_height/2), 0)))
        rs.MoveObjects(tabs, move_over)
       
       
       
        ##To Do: add points to corners of rectangle
       
        #create bounding dimension of leg
        #if less than 10dim
        #elif greater than 10 -- offset
    
    #Leg 01
   
    leg_01 = rs.AddRectangle(rs.WorldXYPlane(), width, height)
    
    leg_01_explode = rs.ExplodeCurves(leg_01)
    
    leg_01_fillet_x = [radius, width - radius, radius, width - radius] 
    leg_01_fillet_y = [radius, radius, height - radius, height - radius]
    leg_01_z_rotations = [180, -90, 90, 0]
    
    for i in range(0, 4):
        #outer_fillets = rs.AddCircle((leg_01_fillet_x[i], leg_01_fillet_y[i], 0), radius)
        outer_fillets_not_rotated = rs.AddArc((leg_01_fillet_x[i], leg_01_fillet_y[i], 0), radius, 90)
        outer_fillets = rs.RotateObject(outer_fillets_not_rotated, (leg_01_fillet_x[i], leg_01_fillet_y[i], 0), leg_01_z_rotations[i])
        
    leg_01_curves = []
    for i in leg_01_explode:
        leg_01_curves.append(i)
        
    leg_01_domains = []
    leg_01_new_dom_a = []
    leg_01_new_dom_b = []
    
    new_domains_list = []
    for curve in leg_01_curves:
        leg_01_domains.append(rs.CurveDomain(curve))
        
    for domain in leg_01_domains:
        leg_01_new_dom_a.append(domain[0] + radius)
        leg_01_new_dom_b.append(domain[1] - radius)
        
    new_domains = list(zip(leg_01_new_dom_a, leg_01_new_dom_b))
    
    for curve, domain in zip(leg_01_curves, new_domains):
        leg_01_outer = rs.TrimCurve(curve, domain)
        
    rs.DeleteObject(leg_01)
    rs.Command("SelAll")
    rs.Command("Join")
    
    if width > 10.375:
        #Establish Irregular Offset of 5 inches on table legs
        five_inch_margin_maker = rs.AddRectangle(rs.WorldXYPlane(), width - 3.5, height)
        offset_direction = (width/2, depth/2, 0)
        move_3 = (1.75, 0, 0)
    
        leg_01_inner = rs.MoveObject(rs.OffsetCurve(five_inch_margin_maker,offset_direction, 3.25), move_3)
    
    
    
    
    
    
    rs.DeleteObject(five_inch_margin_maker)
    
    
    
    
    
print(table_maker(25.5, 15, 38, 0.5, 0.02, 0.5))


"""
    new_domains = []
    new_domains_list = []
    for curve in leg_01_curves:
        leg_01_domains.append(rs.CurveDomain(curve))
    for domain in leg_01_domains:
        new_domains.append(([domain[0] + radius], [domain[1] - radius]))
        for i in new_domains:
            print i
            
            
        leg_01_new_dom_a.append(domain[0] + radius)
        leg_01_new_dom_b.append(domain[1] - radius)
        
        
        """