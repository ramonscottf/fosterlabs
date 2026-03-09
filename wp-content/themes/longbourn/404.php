<?php
/**
 * 404 page template
 *
 * @package Longbourn
 */

get_header();
?>

<div class="section" style="min-height:60vh;display:flex;align-items:center;">
    <div class="container">
        <div class="featured-text">
            <h1 style="font-size:6rem;color:var(--color-forest);margin-bottom:var(--spacing-sm);">404</h1>
            <h2>Page Not Found</h2>
            <p>The page you are looking for may have been moved or no longer exists. Let us help you find your way.</p>
            <div style="margin-top:var(--spacing-md);display:flex;gap:var(--spacing-sm);justify-content:center;flex-wrap:wrap;">
                <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="btn btn--primary">Return Home</a>
                <?php if ( class_exists( 'WooCommerce' ) ) : ?>
                    <a href="<?php echo esc_url( wc_get_page_permalink( 'shop' ) ); ?>" class="btn btn--outline-dark">Browse Shop</a>
                <?php endif; ?>
            </div>
        </div>
    </div>
</div>

<?php get_footer(); ?>
