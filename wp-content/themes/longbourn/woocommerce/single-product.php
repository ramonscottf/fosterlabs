<?php
/**
 * Single product template override
 *
 * @package Longbourn
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

get_header();
?>

<div class="page-content" style="padding-top:var(--spacing-md);">
    <div class="container">
        <?php woocommerce_breadcrumb(); ?>

        <?php while ( have_posts() ) : the_post(); ?>
            <?php wc_get_template_part( 'content', 'single-product' ); ?>
        <?php endwhile; ?>
    </div>
</div>

<!-- Related Products Section -->
<section class="section section--rose">
    <div class="container">
        <div class="featured-text">
            <h2>You May Also Like</h2>
        </div>
    </div>
</section>

<?php get_footer(); ?>
