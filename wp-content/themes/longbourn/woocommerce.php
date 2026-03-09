<?php
/**
 * WooCommerce main template
 *
 * @package Longbourn
 */

get_header();
?>

<?php if ( is_shop() || is_product_category() || is_product_tag() ) : ?>
    <div class="page-header">
        <div class="container">
            <?php if ( is_shop() ) : ?>
                <h1>Our Papers & Provisions</h1>
                <p>Hand-pressed heirloom stationery for meaningful moments</p>
            <?php else : ?>
                <h1><?php woocommerce_page_title(); ?></h1>
                <?php
                $term_description = term_description();
                if ( $term_description ) :
                    echo '<p>' . wp_kses_post( $term_description ) . '</p>';
                endif;
                ?>
            <?php endif; ?>
        </div>
    </div>
<?php endif; ?>

<div class="page-content">
    <div class="container">
        <div class="woocommerce-content">
            <?php woocommerce_content(); ?>
        </div>
    </div>
</div>

<?php get_footer(); ?>
