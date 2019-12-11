'''
    Glyph Proofer
    
    This must be used within the Drawbot extension for RoboFont.
'''

f = CurrentFont()

# settings
glyphScale = 0.6
canvasWidth = canvasHeight = 850
captionSize = 13
captionColor = 1, 0, 0

# collect vertical metrics
metricsY = {
    0,
    f.info.descender,
    f.info.xHeight,
    f.info.capHeight,
    f.info.ascender,
}

# get box height
boxHeight = (max(metricsY) - min(metricsY)) * glyphScale
boxY = (canvasHeight - boxHeight) * 0.5

# get glyph names
glyphNames = f.selectedGlyphNames if len(f.selectedGlyphs) else f.keys()

# draw glyphs
for glyphName in f.glyphOrder:
    if not glyphName in glyphNames:
        continue

    # get glyph
    g = f[glyphName]
    boxWidth = g.width * glyphScale

    # make new page
    newPage(canvasWidth, canvasHeight)

    # calculate origin position
    x = (canvasWidth - boxWidth) * 0.5
    y = boxY + abs(f.info.descender) * glyphScale

    # collect horizontal metrics
    guidesX = {x, x + boxWidth}

    # --------
    # draw box
    # --------

    save()
    fill(0.9)
    rect(x, boxY, boxWidth, boxHeight)
    restore()

    # -----------
    # draw guides
    # -----------

    save()
    lineDash(6, 3)
    stroke(0.5)

    # draw guides x
    for guideX in guidesX:
        line((guideX, 0), (guideX, height()))

    # draw guides y
    for guideY in metricsY:
        guideY = y + guideY * glyphScale
        line((0, guideY), (width(), guideY))

    restore()

    # ----------
    # draw glyph
    # ----------

    save()
    fill(None)
    stroke(0.5)
    strokeWidth(1)
    lineJoin('round')
    translate(x, y)
    scale(glyphScale)
    drawGlyph(g)
    restore()

    # ------------
    # draw points
    # ------------
    
    oncurveSize = 6
    
    offcurveSize = 4
    
    save()
    translate(x, y)
    scale(glyphScale)
    for c in g:
        for bPt in c.bPoints:
            print(bPt.type)
            pt = bPt.anchor
            ptX = pt[0]
            ptY = pt[1]
            
            # draw offcurve points
            ptIn = bPt.bcpIn
            ptOut = bPt.bcpOut 
            
            fill(1)
            stroke(1,0,0)
            if abs(ptIn[0]) > 0 or abs(ptIn[1]) > 0:
                
                ptInX = pt[0]+ptIn[0]
                ptInY = pt[1]+ptIn[1]
                line((ptX, ptY), (ptInX, ptInY))
                rect(ptInX - offcurveSize/2, ptInY - offcurveSize/2, offcurveSize, offcurveSize)
                
                
                
            
            if abs(ptOut[0]) > 0 or abs(ptOut[1]) > 0:
                ptOutX = pt[0]+ptOut[0]
                ptOutY = pt[1]+ptOut[1]
                line((ptX, ptY), (ptOutX, ptOutY))
                rect(ptOutX - offcurveSize/2, pt[1]+ptOut[1] - offcurveSize/2, offcurveSize, offcurveSize)
                
                
            # now draw oncurve point so it's on top
            
            fill(1)
            stroke(0,0,1)
            oval(ptX - oncurveSize/2, ptY - oncurveSize/2, oncurveSize, oncurveSize)
            
            # if bPt.type == "line" or bPt.type == "curve":
            #     rect(pt.x - oncurveSize/2, pt.y - oncurveSize/2, oncurveSize, oncurveSize)
            # if bPt.type == "offcurve":
            #     rect(pt.x - offcurveSize/2, pt.y - offcurveSize/2, offcurveSize, offcurveSize)
        # for s in c:
        #     for pt in s:
        #         if pt.type == "line" or pt.type == "curve":
        #             rect(pt.x - oncurveSize/2, pt.y - oncurveSize/2, oncurveSize, oncurveSize)
        #         if pt.type == "offcurve":
        #             rect(pt.x - offcurveSize/2, pt.y - offcurveSize/2, offcurveSize, offcurveSize)
                    
        #             help(pt)
                    
            

    restore()
    
    # ------------
    # draw anchors
    # ------------

    # radius = 10
    # save()
    # fill(None)
    # stroke(1, 0, 0)
    # translate(x, y)
    # for anchor in g.anchors:
    #     aX, aY = anchor.position
    #     aX *= glyphScale
    #     aY *= glyphScale
    #     oval(aX - radius, aY - radius, radius * 2, radius * 2)
    #     line((aX - radius, aY), (aX + radius, aY))
    #     line((aX, aY - radius), (aX, aY + radius))
    # restore()

    # ------------
    # draw caption
    # ------------

    captionX = captionSize
    captionW = width() - captionSize * 2
    captionH = captionSize * 2

    save()
    font('Recursive Mono Lnr b027st')
    fontSize(captionSize)
    fill(*captionColor)

    # top
    captionY = height() - captionSize * 3
    captionBox = captionX, captionY, captionW, captionH
    textBox(g.name, captionBox, align='left')
    if g.unicode:
        uni = str(hex(g.unicode)).replace("0x", '')
        uni = uni.zfill(4).upper()
        textBox(uni, captionBox, align='right')

    # bottom
    captionY = 0
    captionBox = captionX, captionY, captionW, captionH
    textBox('%.2f' % g.width, captionBox, align='center')
    if g.bounds:
        textBox('%.2f' % g.leftMargin, captionBox, align='left')
        textBox('%.2f' % g.rightMargin, captionBox, align='right')

    restore()