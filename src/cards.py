from datetime import date
from io import BytesIO
from typing import List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from .suggest import suggest_for_day
from .models import Dish

def generate_cook_cards_pdf(day: date, dishes: Optional[List[Dish]] = None) -> BytesIO:
    """Generate Pokémon-style cook cards PDF for a given date."""
    if dishes is None:
        plan = suggest_for_day(day)
        dishes = []
        for meal_slots in plan.values():
            dishes.extend(meal_slots.values())
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        spaceAfter=20
    )
    
    card_title_style = ParagraphStyle(
        'CardTitle',
        parent=styles['Heading2'],
        fontSize=16,
        alignment=TA_CENTER,
        textColor=colors.darkred,
        spaceAfter=10
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=6
    )
    
    story = []
    
    # Title
    title = Paragraph(f"Nigela Cook Cards • {day.strftime('%B %d, %Y')}", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Generate cards for each dish
    for i, dish in enumerate(dishes):
        if i > 0:
            story.append(Spacer(1, 30))
        
        # Card border and content
        card_data = []
        
        # Dish name and rarity
        rarity_color = {
            'common': colors.green,
            'rare': colors.blue,
            'epic': colors.purple,
            'legendary': colors.gold
        }.get(dish.rarity, colors.black)
        
        name_cell = Paragraph(f"<b>{dish.name}</b>", card_title_style)
        rarity_cell = Paragraph(f"★ {dish.rarity.upper()}", 
                               ParagraphStyle('Rarity', parent=normal_style, 
                                            textColor=rarity_color, alignment=TA_CENTER))
        card_data.append([name_cell, rarity_cell])
        
        # Stats row
        stats = f"Cook Time: {dish.cook_minutes}min | Difficulty: {'★' * dish.difficulty} | Meal: {dish.meal_type.title()}"
        stats_cell = Paragraph(stats, normal_style)
        card_data.append([stats_cell, ""])
        
        # Tags
        tags_text = " • ".join([t.replace(":", " ") for t in dish.tags[:4]])  # Show first 4 tags
        tags_cell = Paragraph(f"<i>Tags: {tags_text}</i>", normal_style)
        card_data.append([tags_cell, ""])
        
        # Ingredients
        ing_text = ", ".join([f"{i.item}" + (f" ({i.qty}{i.unit})" if i.qty > 0 else "") 
                             for i in dish.ingredients[:6]])  # Show first 6 ingredients
        if len(dish.ingredients) > 6:
            ing_text += "..."
        ing_cell = Paragraph(f"<b>Ingredients:</b> {ing_text}", normal_style)
        card_data.append([ing_cell, ""])
        
        # Flavor text
        if dish.flavor_text:
            flavor_cell = Paragraph(f'<i>"{dish.flavor_text}"</i>', 
                                  ParagraphStyle('Flavor', parent=normal_style, 
                                               textColor=colors.darkgreen))
            card_data.append([flavor_cell, ""])
        
        # Steps (first 3)
        steps_text = " → ".join(dish.steps[:3])
        if len(dish.steps) > 3:
            steps_text += "..."
        steps_cell = Paragraph(f"<b>Quick Steps:</b> {steps_text}", normal_style)
        card_data.append([steps_cell, ""])
        
        # Variants if available
        if hasattr(dish, 'variant_adults') and dish.variant_adults:
            variant_cell = Paragraph(f"<b>Adult variant:</b> {dish.variant_adults}", normal_style)
            card_data.append([variant_cell, ""])
        
        if hasattr(dish, 'variant_kids') and dish.variant_kids:
            variant_cell = Paragraph(f"<b>Kids variant:</b> {dish.variant_kids}", normal_style)
            card_data.append([variant_cell, ""])
        
        # Create the card table
        card_table = Table(card_data, colWidths=[5*inch, 1.5*inch])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(card_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer
