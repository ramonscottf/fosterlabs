<?php
/**
 * Longbourn Papers Theme Functions
 *
 * @package Longbourn
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'LONGBOURN_VERSION', '1.0.0' );

/**
 * Theme Setup
 */
function longbourn_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'custom-logo', array(
        'height'      => 100,
        'width'       => 300,
        'flex-height' => true,
        'flex-width'  => true,
    ) );
    add_theme_support( 'html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
    ) );
    add_theme_support( 'automatic-feed-links' );

    // WooCommerce support
    add_theme_support( 'woocommerce' );
    add_theme_support( 'wc-product-gallery-zoom' );
    add_theme_support( 'wc-product-gallery-lightbox' );
    add_theme_support( 'wc-product-gallery-slider' );

    // Register nav menus
    register_nav_menus( array(
        'primary'   => __( 'Primary Menu', 'longbourn' ),
        'footer'    => __( 'Footer Menu', 'longbourn' ),
    ) );

    // Image sizes
    add_image_size( 'longbourn-hero', 1920, 800, true );
    add_image_size( 'longbourn-product', 600, 600, true );
    add_image_size( 'longbourn-blog', 800, 450, true );
    add_image_size( 'longbourn-collection', 800, 600, true );
}
add_action( 'after_setup_theme', 'longbourn_setup' );

/**
 * Enqueue Styles & Scripts
 */
function longbourn_scripts() {
    // Google Fonts
    wp_enqueue_style(
        'longbourn-fonts',
        'https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500;600;700&display=swap',
        array(),
        null
    );

    // Main stylesheet
    wp_enqueue_style(
        'longbourn-style',
        get_stylesheet_uri(),
        array( 'longbourn-fonts' ),
        LONGBOURN_VERSION
    );

    // Theme JavaScript
    wp_enqueue_script(
        'longbourn-scripts',
        get_template_directory_uri() . '/assets/js/main.js',
        array(),
        LONGBOURN_VERSION,
        true
    );
}
add_action( 'wp_enqueue_scripts', 'longbourn_scripts' );

/**
 * Register Widget Areas
 */
function longbourn_widgets_init() {
    register_sidebar( array(
        'name'          => __( 'Footer Column 1', 'longbourn' ),
        'id'            => 'footer-1',
        'before_widget' => '<div class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h4>',
        'after_title'   => '</h4>',
    ) );

    register_sidebar( array(
        'name'          => __( 'Footer Column 2', 'longbourn' ),
        'id'            => 'footer-2',
        'before_widget' => '<div class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h4>',
        'after_title'   => '</h4>',
    ) );

    register_sidebar( array(
        'name'          => __( 'Footer Column 3', 'longbourn' ),
        'id'            => 'footer-3',
        'before_widget' => '<div class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h4>',
        'after_title'   => '</h4>',
    ) );

    register_sidebar( array(
        'name'          => __( 'Shop Sidebar', 'longbourn' ),
        'id'            => 'shop-sidebar',
        'before_widget' => '<div class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h4>',
        'after_title'   => '</h4>',
    ) );
}
add_action( 'widgets_init', 'longbourn_widgets_init' );

/**
 * WooCommerce: Change products per row
 */
function longbourn_wc_products_per_row() {
    return 4;
}
add_filter( 'loop_shop_columns', 'longbourn_wc_products_per_row' );

/**
 * WooCommerce: Products per page
 */
function longbourn_wc_products_per_page() {
    return 12;
}
add_filter( 'loop_shop_per_page', 'longbourn_wc_products_per_page' );

/**
 * WooCommerce: Remove default wrapper
 */
remove_action( 'woocommerce_before_main_content', 'woocommerce_output_content_wrapper', 10 );
remove_action( 'woocommerce_after_main_content', 'woocommerce_output_content_wrapper_end', 10 );

function longbourn_wc_wrapper_start() {
    echo '<div class="container"><div class="woocommerce-content">';
}
add_action( 'woocommerce_before_main_content', 'longbourn_wc_wrapper_start', 10 );

function longbourn_wc_wrapper_end() {
    echo '</div></div>';
}
add_action( 'woocommerce_after_main_content', 'longbourn_wc_wrapper_end', 10 );

/**
 * WooCommerce: Remove sidebar from shop
 */
remove_action( 'woocommerce_sidebar', 'woocommerce_get_sidebar', 10 );

/**
 * Custom excerpt length
 */
function longbourn_excerpt_length( $length ) {
    return 25;
}
add_filter( 'excerpt_length', 'longbourn_excerpt_length' );

/**
 * Custom excerpt more text
 */
function longbourn_excerpt_more( $more ) {
    return '&hellip;';
}
add_filter( 'excerpt_more', 'longbourn_excerpt_more' );

/**
 * Add body classes
 */
function longbourn_body_classes( $classes ) {
    if ( is_front_page() ) {
        $classes[] = 'front-page';
    }
    if ( class_exists( 'WooCommerce' ) ) {
        if ( is_shop() || is_product_category() || is_product_tag() ) {
            $classes[] = 'shop-page';
        }
    }
    return $classes;
}
add_filter( 'body_class', 'longbourn_body_classes' );

/**
 * Customizer settings
 */
function longbourn_customize_register( $wp_customize ) {
    // Hero Section
    $wp_customize->add_section( 'longbourn_hero', array(
        'title'    => __( 'Hero Section', 'longbourn' ),
        'priority' => 30,
    ) );

    $wp_customize->add_setting( 'longbourn_hero_title', array(
        'default'           => 'Elevate Every Gift',
        'sanitize_callback' => 'sanitize_text_field',
    ) );
    $wp_customize->add_control( 'longbourn_hero_title', array(
        'label'   => __( 'Hero Title', 'longbourn' ),
        'section' => 'longbourn_hero',
        'type'    => 'text',
    ) );

    $wp_customize->add_setting( 'longbourn_hero_subtitle', array(
        'default'           => 'Hand-pressed heirloom stationery crafted with traditional techniques on rich cotton paper.',
        'sanitize_callback' => 'sanitize_text_field',
    ) );
    $wp_customize->add_control( 'longbourn_hero_subtitle', array(
        'label'   => __( 'Hero Subtitle', 'longbourn' ),
        'section' => 'longbourn_hero',
        'type'    => 'textarea',
    ) );

    $wp_customize->add_setting( 'longbourn_hero_cta_text', array(
        'default'           => 'Shop Tags',
        'sanitize_callback' => 'sanitize_text_field',
    ) );
    $wp_customize->add_control( 'longbourn_hero_cta_text', array(
        'label'   => __( 'CTA Button Text', 'longbourn' ),
        'section' => 'longbourn_hero',
        'type'    => 'text',
    ) );

    $wp_customize->add_setting( 'longbourn_hero_cta_url', array(
        'default'           => '/shop',
        'sanitize_callback' => 'esc_url_raw',
    ) );
    $wp_customize->add_control( 'longbourn_hero_cta_url', array(
        'label'   => __( 'CTA Button URL', 'longbourn' ),
        'section' => 'longbourn_hero',
        'type'    => 'url',
    ) );

    $wp_customize->add_setting( 'longbourn_hero_image', array(
        'sanitize_callback' => 'absint',
    ) );
    $wp_customize->add_control( new WP_Customize_Media_Control( $wp_customize, 'longbourn_hero_image', array(
        'label'     => __( 'Hero Background Image', 'longbourn' ),
        'section'   => 'longbourn_hero',
        'mime_type' => 'image',
    ) ) );

    // Contact Info
    $wp_customize->add_section( 'longbourn_contact', array(
        'title'    => __( 'Contact Information', 'longbourn' ),
        'priority' => 35,
    ) );

    $wp_customize->add_setting( 'longbourn_phone', array(
        'default'           => '801-205-6642',
        'sanitize_callback' => 'sanitize_text_field',
    ) );
    $wp_customize->add_control( 'longbourn_phone', array(
        'label'   => __( 'Phone Number', 'longbourn' ),
        'section' => 'longbourn_contact',
        'type'    => 'text',
    ) );

    $wp_customize->add_setting( 'longbourn_email', array(
        'default'           => 'alexandra@longbournpapers.com',
        'sanitize_callback' => 'sanitize_email',
    ) );
    $wp_customize->add_control( 'longbourn_email', array(
        'label'   => __( 'Email Address', 'longbourn' ),
        'section' => 'longbourn_contact',
        'type'    => 'email',
    ) );

    $wp_customize->add_setting( 'longbourn_address', array(
        'default'           => 'PO Box 22, Farmington UT 84025',
        'sanitize_callback' => 'sanitize_text_field',
    ) );
    $wp_customize->add_control( 'longbourn_address', array(
        'label'   => __( 'Mailing Address', 'longbourn' ),
        'section' => 'longbourn_contact',
        'type'    => 'text',
    ) );

    // Social Media
    $wp_customize->add_section( 'longbourn_social', array(
        'title'    => __( 'Social Media', 'longbourn' ),
        'priority' => 40,
    ) );

    $social_networks = array( 'instagram', 'facebook', 'pinterest' );
    foreach ( $social_networks as $network ) {
        $wp_customize->add_setting( "longbourn_social_{$network}", array(
            'default'           => '',
            'sanitize_callback' => 'esc_url_raw',
        ) );
        $wp_customize->add_control( "longbourn_social_{$network}", array(
            'label'   => ucfirst( $network ) . ' URL',
            'section' => 'longbourn_social',
            'type'    => 'url',
        ) );
    }
}
add_action( 'customize_register', 'longbourn_customize_register' );

/**
 * Contact form handler (simple built-in form)
 */
function longbourn_handle_contact_form() {
    if ( ! isset( $_POST['longbourn_contact_nonce'] ) || ! wp_verify_nonce( $_POST['longbourn_contact_nonce'], 'longbourn_contact' ) ) {
        return;
    }

    $name    = sanitize_text_field( $_POST['contact_name'] ?? '' );
    $email   = sanitize_email( $_POST['contact_email'] ?? '' );
    $phone   = sanitize_text_field( $_POST['contact_phone'] ?? '' );
    $type    = sanitize_text_field( $_POST['contact_type'] ?? '' );
    $message = sanitize_textarea_field( $_POST['contact_message'] ?? '' );

    if ( empty( $name ) || empty( $email ) || empty( $message ) ) {
        return;
    }

    $to      = get_theme_mod( 'longbourn_email', 'alexandra@longbournpapers.com' );
    $subject = sprintf( '[Longbourn Papers] %s from %s', $type, $name );
    $body    = sprintf(
        "Name: %s\nEmail: %s\nPhone: %s\nType: %s\n\nMessage:\n%s",
        $name, $email, $phone, $type, $message
    );
    $headers = array( 'Content-Type: text/plain; charset=UTF-8', "Reply-To: {$email}" );

    wp_mail( $to, $subject, $body, $headers );
}
add_action( 'init', 'longbourn_handle_contact_form' );
