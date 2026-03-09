# Longbourn Papers - WordPress Theme Setup Guide

## Overview
This is a custom WordPress theme for Longbourn Papers, designed to replicate the existing Shopify store. It includes full WooCommerce integration for product management and e-commerce functionality.

## Requirements
- WordPress 6.0+
- PHP 8.0+
- WooCommerce 8.0+ plugin

## Installation

1. **Install WordPress** on your hosting environment
2. **Copy the theme**: Upload the `longbourn` folder to `wp-content/themes/`
3. **Activate the theme**: Go to Appearance > Themes > Activate "Longbourn Papers"
4. **Install WooCommerce**: Plugins > Add New > Search "WooCommerce" > Install & Activate

## Theme Setup

### 1. Create Pages
Create the following WordPress pages and assign their templates:

| Page Title | Template (Page Attributes) | Slug |
|---|---|---|
| Home | Front Page | `home` |
| About | About Page | `about` |
| Contact | Contact Page | `contact` |
| The Art of Letterpress | Art of Letterpress | `the-art-of-letterpress` |

Set "Home" as your static front page: Settings > Reading > "A static page" > Homepage: Home

Create a "Blog" page for the posts page.

### 2. Set Up Menus
Go to Appearance > Menus and create a "Primary Menu":

- Gift Tags (link to product category)
- Grand Tags (link to product category)
- Petite Cards (link to product category)
- Stationery (link to product category)
- Holiday (link to product category)
- Collections (custom link, #)
  - Sympathy (link to product category)
  - Gratitude (link to product category)
  - Celebration (link to product category)
  - Baby (link to product category)
  - Holiday (link to product category)
- Connect (custom link, #)
  - About (page link)
  - Art of Letterpress (page link)
  - Contact (page link)
  - Blog (page link)

Assign to "Primary Menu" location.

### 3. Configure Customizer
Go to Appearance > Customize:

**Hero Section:**
- Hero Title: "Elevate Every Gift"
- Hero Subtitle: "Hand-pressed heirloom stationery..."
- CTA Button Text: "Shop Tags"
- CTA URL: /product-category/gift-tags/
- Upload a hero background image

**Contact Information:**
- Phone: 801-205-6642
- Email: alexandra@longbournpapers.com
- Address: PO Box 22, Farmington UT 84025

**Social Media:**
- Add Instagram, Facebook, Pinterest URLs

**Site Identity:**
- Upload the Longbourn Papers logo

### 4. WooCommerce Product Categories
Create these product categories in WooCommerce:
- Gift Tags
- Grand Tags
- Petite Cards
- Stationery
- Holiday

And these collection categories:
- Sympathy & Support
- Thank You & Gratitude
- Celebration & Congratulations
- Baby
- Our Papers & Provisions

### 5. Import Products
For each product from Shopify, create a WooCommerce product with:
- Product name, description, and images
- Pricing (simple or variable products for items with options)
- Assign to appropriate categories
- Set featured products for homepage display

#### Product Reference (from Shopify):

**Gift Tags** - Letterpress Gift Tags with Satin Ribbon - $24.00
**Grand Tags** - Letterpress Grand Tags with Satin Ribbon - $20.00
**Stationery** - Letterpress Note Card & Envelope Set - $24.00
**Petite Cards** - Letterpress Note Cards - Single: $4.00 / 6-Pack: $18.00

Designs include: Bravo, Celebrate, Congratulations, Blossom, Floral Wreath, Hummingbird, Baby Blue, Baby Blush, Hearts, Nautical, Birthday Cake, Dream, Queen Bee, Laurel, and more.

### 6. Upload Images
- Export all product images from Shopify
- Upload to WordPress Media Library
- Assign to corresponding products
- Upload hero/background images via Customizer

## Theme Files Reference

```
longbourn/
├── style.css              # Main stylesheet + theme info
├── functions.php          # Theme setup, WooCommerce config, customizer
├── header.php             # Site header + navigation
├── footer.php             # Site footer
├── front-page.php         # Homepage template
├── index.php              # Blog listing
├── single.php             # Single blog post
├── page.php               # Default page template
├── page-about.php         # About page template
├── page-contact.php       # Contact page template
├── page-letterpress.php   # Art of Letterpress template
├── archive.php            # Blog archive/category
├── search.php             # Search results
├── 404.php                # 404 error page
├── sidebar.php            # Sidebar widget area
├── woocommerce.php        # WooCommerce shop/category template
├── woocommerce/
│   └── single-product.php # Single product page override
├── assets/
│   ├── css/               # Additional stylesheets
│   ├── js/
│   │   └── main.js        # Theme JavaScript
│   └── images/            # Theme images
└── template-parts/        # Reusable template parts
```

## Brand Colors
- Forest Green: #1d322d
- Cream: #faf7f4
- Sage: #e2eded
- Rose: #f1e9e7
- Burgundy: #6b2d3e
- Gold: #b8973e

## Fonts
- Headings: EB Garamond (serif)
- Body: Inter (sans-serif)
