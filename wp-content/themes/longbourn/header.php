<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="site-header">
    <div class="container">
        <div class="site-branding">
            <?php if ( has_custom_logo() ) : ?>
                <?php the_custom_logo(); ?>
            <?php else : ?>
                <a href="<?php echo esc_url( home_url( '/' ) ); ?>">
                    <?php bloginfo( 'name' ); ?>
                </a>
            <?php endif; ?>
        </div>

        <button class="menu-toggle" aria-label="<?php esc_attr_e( 'Toggle Menu', 'longbourn' ); ?>" aria-expanded="false">
            <span></span>
            <span></span>
            <span></span>
        </button>

        <nav class="main-navigation" role="navigation" aria-label="<?php esc_attr_e( 'Primary Menu', 'longbourn' ); ?>">
            <?php
            wp_nav_menu( array(
                'theme_location' => 'primary',
                'container'      => false,
                'fallback_cb'    => 'longbourn_fallback_menu',
            ) );
            ?>
        </nav>

        <div class="header-utilities">
            <?php if ( class_exists( 'WooCommerce' ) ) : ?>
                <a href="<?php echo esc_url( wc_get_page_permalink( 'myaccount' ) ); ?>" aria-label="<?php esc_attr_e( 'My Account', 'longbourn' ); ?>">
                    Account
                </a>
                <a href="<?php echo esc_url( wc_get_cart_url() ); ?>" class="cart-link" aria-label="<?php esc_attr_e( 'View Cart', 'longbourn' ); ?>">
                    Cart
                    <?php if ( WC()->cart && WC()->cart->get_cart_contents_count() > 0 ) : ?>
                        <span class="cart-count"><?php echo esc_html( WC()->cart->get_cart_contents_count() ); ?></span>
                    <?php endif; ?>
                </a>
            <?php endif; ?>
        </div>
    </div>
</header>

<?php
/**
 * Fallback menu if no menu is assigned
 */
function longbourn_fallback_menu() {
    echo '<ul>';
    echo '<li><a href="' . esc_url( home_url( '/' ) ) . '">Home</a></li>';
    if ( class_exists( 'WooCommerce' ) ) {
        echo '<li><a href="' . esc_url( wc_get_page_permalink( 'shop' ) ) . '">Shop</a></li>';
    }
    echo '<li><a href="' . esc_url( home_url( '/about/' ) ) . '">About</a></li>';
    echo '<li><a href="' . esc_url( home_url( '/contact/' ) ) . '">Contact</a></li>';
    echo '<li><a href="' . esc_url( home_url( '/blog/' ) ) . '">Blog</a></li>';
    echo '</ul>';
}
