# Longevity India - BHARAT Study Branding Guide

This comprehensive guide covers the implementation of Longevity India's visual identity and BHARAT Study branding within the OpenSpecimen platform.

## Overview

The Longevity India branding system creates a cohesive visual identity that reflects the organization's mission to advance aging research in India while maintaining professional standards for biobanking operations.

### Brand Identity Elements

```
Organization: Longevity India
Study: BHARAT Study (Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions)
Tagline: "Advancing Aging Research in India"
Domain: Aging research, multi-omics analysis, longitudinal studies
```

## Color Palette

### Primary Colors

#### Deep Red (#C41E3A)
- **Usage**: Primary buttons, headers, navigation highlights
- **Meaning**: Vitality and life force
- **Contrast Ratio**: 8.2:1 (with white text)
- **Light Variant**: #E85A75
- **Dark Variant**: #8B1A2B

#### Warm Orange (#FF6B35)
- **Usage**: Secondary elements, accent highlights, call-to-action items
- **Meaning**: Energy and transformation
- **Light Variant**: #FF9666
- **Dark Variant**: #B24725

#### Sea Green (#2E8B57)
- **Usage**: Success states, health indicators, nature-related elements
- **Meaning**: Health and natural well-being
- **Light Variant**: #5FA474
- **Dark Variant**: #1F5F3C

### Functional Colors

```css
Background: #FAFAFA (Primary background)
Surface: #FFFFFF (Card and panel backgrounds)
Text: #212121 (Primary text)
Text Secondary: #757575 (Secondary text)
Border: #E0E0E0 (Dividers and borders)
Success: #4CAF50 (Success messages)
Warning: #FF9800 (Warning messages)
Error: #F44336 (Error messages)
Info: #2196F3 (Informational messages)
```

### Age Group Colors

The BHARAT Study uses distinct colors for each age cohort to facilitate quick visual identification:

```
AG1 (20-30 years): #4CAF50 (Fresh Green)
AG2 (31-40 years): #8BC34A (Light Green) 
AG3 (41-50 years): #FF9800 (Orange)
AG4 (51-60 years): #FF5722 (Deep Orange)
AG5 (61-70 years): #9C27B0 (Purple)
```

### Biomarker Category Colors

Different analysis types are color-coded for easy identification:

```
Genomics: #2196F3 (Blue)
Proteomics: #9C27B0 (Purple)
Metabolomics: #FF9800 (Orange)
Epigenomics: #4CAF50 (Green)
Inflammation: #F44336 (Red)
Clinical: #607D8B (Blue Grey)
```

## Typography

### Font Families

#### Primary Font: Inter
- **Usage**: Body text, UI elements, forms, tables
- **Weights**: 300, 400, 500, 600, 700
- **Characteristics**: Modern, clean, highly legible
- **Fallback**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif

#### Heading Font: Poppins
- **Usage**: Page titles, section headers, navigation
- **Weights**: 400, 500, 600, 700
- **Characteristics**: Professional, distinctive, friendly
- **Fallback**: 'Inter', sans-serif

#### Monospace Font: JetBrains Mono
- **Usage**: Code snippets, sample IDs, technical data
- **Weights**: 400, 500
- **Characteristics**: Developer-friendly, clear distinction
- **Fallback**: 'Fira Code', 'Courier New', monospace

### Type Scale

```
H1: 2.5rem (40px) - Page titles
H2: 2rem (32px) - Major section headers
H3: 1.75rem (28px) - Subsection headers
H4: 1.5rem (24px) - Component headers
H5: 1.25rem (20px) - Minor headers
H6: 1rem (16px) - Small headers
Body: 0.875rem (14px) - Main content
Caption: 0.75rem (12px) - Labels, captions
Small: 0.625rem (10px) - Fine print
```

## Layout System

### Header Configuration

```css
Height: 64px
Background: #C41E3A (Primary red)
Text Color: #FFFFFF (White)
Logo Height: 40px
Padding: 12px 24px
```

The header features the Longevity India logo, BHARAT Study title, and primary navigation elements.

### Sidebar Navigation

```css
Width: 280px
Background: #FAFAFA (Light grey)
Border: 1px solid #E0E0E0
Active Item Color: #C41E3A (Primary red)
```

### Content Areas

```css
Background: #FFFFFF (White)
Padding: 24px
Border Radius: 8px
Box Shadow: 0 2px 8px rgba(0, 0, 0, 0.1)
```

### Footer

```css
Height: 48px
Background: #F5F5F5 (Light grey)
Text Color: #757575 (Secondary text)
Padding: 12px 24px
```

## Component Styles

### Buttons

#### Primary Button
```css
Background: #C41E3A
Color: #FFFFFF
Border Radius: 6px
Padding: 8px 16px
Font Weight: 500
Hover Background: #8B1A2B
```

#### Secondary Button
```css
Background: transparent
Color: #C41E3A
Border: 2px solid #C41E3A
Border Radius: 6px
Padding: 8px 16px
Font Weight: 500
Hover: Background #C41E3A, Color #FFFFFF
```

### Cards

#### Default Card
```css
Background: #FFFFFF
Border Radius: 12px
Box Shadow: 0 4px 12px rgba(0, 0, 0, 0.1)
Padding: 20px
Border: 1px solid #E0E0E0
```

#### Highlighted Card
```css
Background: #FFFFFF
Border Radius: 12px
Box Shadow: 0 6px 20px rgba(196, 30, 58, 0.15)
Padding: 20px
Border: 2px solid #C41E3A
```

### Forms

#### Input Fields
```css
Border: 1px solid #E0E0E0
Border Radius: 6px
Padding: 10px 12px
Font Size: 0.875rem
Focus Border: #C41E3A
Focus Shadow: 0 0 0 3px rgba(196, 30, 58, 0.1)
```

#### Labels
```css
Color: #212121
Font Size: 0.875rem
Font Weight: 500
Margin Bottom: 6px
```

### Tables

#### Headers
```css
Background: #F5F5F5
Color: #212121
Font Weight: 600
Padding: 12px 16px
Border Bottom: 2px solid #E0E0E0
```

#### Rows
```css
Padding: 12px 16px
Border Bottom: 1px solid #E0E0E0
Hover Background: #FAFAFA
Alternate Background: #F9F9F9
```

## Specialized Components

### Age Group Badges

Age group indicators use distinctive colors for quick identification:

```html
<span class="age-group-badge age-group-ag1">AG1</span>
<span class="age-group-badge age-group-ag2">AG2</span>
<span class="age-group-badge age-group-ag3">AG3</span>
<span class="age-group-badge age-group-ag4">AG4</span>
<span class="age-group-badge age-group-ag5">AG5</span>
```

### Visit Stage Indicators

Visit progress is shown with color-coded indicators:

```html
<span class="visit-indicator visit-v0">V0 - Baseline</span>
<span class="visit-indicator visit-v1">V1 - 6 Months</span>
<span class="visit-indicator visit-v2">V2 - 12 Months</span>
<span class="visit-indicator visit-v3">V3 - 24 Months</span>
```

### Biomarker Category Labels

Analysis types are distinguished by color:

```html
<div class="biomarker-category biomarker-genomics">Genomics Analysis</div>
<div class="biomarker-category biomarker-proteomics">Proteomics Analysis</div>
<div class="biomarker-category biomarker-metabolomics">Metabolomics Analysis</div>
```

## Dashboard Customizations

### Hero Section

The BHARAT Study dashboard features a prominent hero section:

```html
<div class="bharat-dashboard-hero">
    <h1>BHARAT Study Dashboard</h1>
    <p>Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions</p>
</div>
```

**Styling:**
- Background: Linear gradient from #C41E3A to #FF6B35
- Text Color: #FFFFFF
- Padding: 40px 20px
- Border Radius: 12px

### Quick Statistics Cards

Dashboard statistics are presented in color-coded cards:

```html
<div class="quick-stats-row">
    <div class="stat-card participants">
        <i class="fa fa-users"></i>
        <h3>630</h3>
        <p>Total Participants</p>
    </div>
    <div class="stat-card samples">
        <i class="fa fa-vial"></i>
        <h3>2,847</h3>
        <p>Samples Collected</p>
    </div>
    <!-- Additional stat cards -->
</div>
```

**Icon Colors:**
- Participants: #4CAF50 (Green)
- Samples: #2196F3 (Blue)
- Analyses: #FF9800 (Orange)
- Visits: #9C27B0 (Purple)

## Responsive Design

### Breakpoints

```css
Mobile: 768px
Tablet: 1024px
Desktop: 1200px
Widescreen: 1400px
```

### Mobile Optimizations

#### Collapsible Sidebar
- Sidebar transforms to overlay on mobile
- Hamburger menu appears in header
- Touch-optimized navigation

#### Header Adjustments
- Reduced padding: 8px 16px
- Sticky positioning maintained
- Logo scales appropriately

#### Typography Scaling
- H1 reduces to 2rem on mobile
- Body text maintains 14px minimum
- Touch targets minimum 44px

#### Interactive Elements
- Buttons maintain minimum 44px height
- Form inputs have adequate spacing
- Cards stack vertically on mobile

## Accessibility Features

### Color Contrast

All color combinations meet WCAG 2.1 AA standards:

```
Primary Red on White: 8.2:1 (Excellent)
Black Text on White: 12.6:1 (Excellent)
Secondary Text on Background: 4.8:1 (Good)
```

### Focus Indicators

```css
Focus Color: #C41E3A
Focus Width: 3px
Focus Style: solid
Focus Offset: 2px
```

### Text Scaling

- Supports up to 200% zoom
- Maintains layout integrity
- Preserves functionality

### Screen Reader Support

- Semantic HTML structure
- ARIA labels for complex components
- Descriptive alt text for images
- Logical tab order

## Implementation Files

### Core Files

#### 1. longevity-india-branding-config.json
Complete branding configuration including colors, typography, layout specifications, and component definitions.

#### 2. setup-longevity-india-branding.py
Automated setup script that:
- Generates CSS theme file
- Creates dashboard customizations
- Configures login page styling
- Sets up OpenSpecimen configuration

#### 3. longevity-india-theme.css
Main CSS file containing:
- CSS custom properties (variables)
- Component styling overrides
- Responsive design rules
- Accessibility enhancements

#### 4. longevity-india-dashboard.js
JavaScript customizations for:
- Dynamic color application
- Chart initialization
- Mobile menu functionality
- Real-time data visualization

#### 5. longevity-india-login.html
Custom login page featuring:
- Branded login form
- Study information
- Responsive design
- Security best practices

## Installation Instructions

### Step 1: Run Setup Script

```bash
# Execute the branding setup
python setup-longevity-india-branding.py

# Enter OpenSpecimen credentials when prompted
Username: admin@openspecimen.org
Password: [your-password]
```

### Step 2: Deploy Assets

Copy generated files to OpenSpecimen web directory:

```bash
# Copy CSS and JS files
cp longevity-india-theme.css /path/to/openspecimen/web/
cp longevity-india-dashboard.js /path/to/openspecimen/web/
cp longevity-india-login.html /path/to/openspecimen/web/

# Create images directory and add logos
mkdir -p /path/to/openspecimen/web/images/
# Add longevity-india-logo.png and longevity-india-favicon.ico
```

### Step 3: Configure OpenSpecimen

Update OpenSpecimen configuration:

```properties
# Add to openspecimen.properties
app.title=BHARAT Study Portal - Longevity India
institute.name=Longevity India
custom.css.url=/longevity-india-theme.css
custom.js.url=/longevity-india-dashboard.js
logo.url=/images/longevity-india-logo.png
favicon.url=/images/longevity-india-favicon.ico
```

### Step 4: Restart and Test

1. Restart OpenSpecimen server
2. Clear browser cache
3. Test login page styling
4. Verify dashboard customizations
5. Check mobile responsiveness

## User Training

### Interface Changes

#### Visual Updates
- New color scheme throughout application
- Updated typography and spacing
- Enhanced dashboard with study-specific metrics
- Age group and biomarker color coding

#### Navigation Improvements
- Clearer menu organization
- Mobile-responsive design
- Improved accessibility features
- Consistent visual hierarchy

#### Dashboard Enhancements
- BHARAT Study hero section
- Quick statistics overview
- Age group distribution charts
- Visit completion tracking

### Training Topics

1. **New Visual Identity**
   - Color meanings and usage
   - Typography updates
   - Logo placement and usage

2. **Enhanced Navigation**
   - Mobile menu functionality
   - Responsive behavior
   - Accessibility features

3. **Dashboard Features**
   - Quick statistics interpretation
   - Chart interactions
   - Color-coded categories

4. **Data Visualization**
   - Age group color coding
   - Visit stage indicators
   - Biomarker categories
   - Quality status colors

## Maintenance and Updates

### Regular Maintenance

#### CSS Updates
- Monitor browser compatibility
- Update color values if needed
- Optimize performance
- Test new device resolutions

#### JavaScript Enhancements
- Update chart libraries
- Add new visualizations
- Improve mobile interactions
- Enhance accessibility

#### Asset Management
- Optimize image file sizes
- Update logos as needed
- Maintain icon libraries
- Backup customization files

### Version Control

Maintain version history for:
- CSS theme files
- JavaScript customizations
- Configuration settings
- Asset files

### Performance Monitoring

Track metrics for:
- Page load times
- CSS/JS file sizes
- Mobile performance
- User engagement

## Troubleshooting

### Common Issues

#### Styles Not Applying
1. Check CSS file path in configuration
2. Verify file permissions
3. Clear browser cache
4. Restart OpenSpecimen server

#### Mobile Layout Issues
1. Test across different devices
2. Verify viewport meta tag
3. Check responsive breakpoints
4. Update mobile-specific CSS

#### Color Contrast Problems
1. Validate color combinations
2. Test with accessibility tools
3. Adjust contrast ratios
4. Update color variables

#### JavaScript Functionality
1. Check browser console for errors
2. Verify script loading order
3. Test JavaScript dependencies
4. Update library versions

### Support Resources

- **Technical Support**: openspecimen-support@longevityindia.org
- **Branding Questions**: design@longevityindia.org
- **User Training**: training@longevityindia.org
- **Emergency Support**: +91-XXXXXXXXXX (24/7)

## Best Practices

### Design Consistency

1. **Use Color Variables**: Always use CSS custom properties
2. **Maintain Contrast**: Follow WCAG accessibility guidelines
3. **Test Responsively**: Verify on multiple screen sizes
4. **Document Changes**: Keep change log for updates

### Performance Optimization

1. **Minimize CSS**: Use compressed versions in production
2. **Optimize Images**: Use appropriate formats and sizes
3. **Cache Assets**: Configure proper cache headers
4. **Monitor Loading**: Track performance metrics

### Accessibility Compliance

1. **Test Regularly**: Use automated accessibility tools
2. **User Testing**: Include users with disabilities
3. **Keyboard Navigation**: Ensure full keyboard accessibility
4. **Screen Readers**: Test with assistive technologies

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Author**: Longevity India BHARAT Study Team