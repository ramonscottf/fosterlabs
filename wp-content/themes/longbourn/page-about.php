<?php
/**
 * Template Name: About Page
 * About page template for Longbourn Papers
 *
 * @package Longbourn
 */

get_header();
?>

<div class="page-header">
    <div class="container">
        <h1>About Longbourn Papers</h1>
    </div>
</div>

<section class="section section--cream">
    <div class="container">
        <div class="about-intro">
            <h2>Our Story</h2>
            <p>Longbourn Papers was born from a love of beautiful stationery and the belief that handwritten correspondence is one of life's greatest luxuries. Every piece we create is designed to make your words feel as special as the sentiment behind them.</p>
        </div>

        <div class="split-content">
            <div class="split-content__image">
                <?php if ( has_post_thumbnail() ) : ?>
                    <?php the_post_thumbnail( 'large' ); ?>
                <?php else : ?>
                    <div style="width:100%;min-height:400px;background:var(--color-sage);display:flex;align-items:center;justify-content:center;">
                        <span style="color:var(--color-text-light);font-family:var(--font-serif);font-size:1.25rem;">About Image</span>
                    </div>
                <?php endif; ?>
            </div>
            <div class="split-content__text">
                <h2>Hand-Pressed Heirloom Stationery</h2>
                <p>We use traditional letterpress techniques to create stationery that is both beautiful and tactile. Each piece is printed on rich cotton paper, resulting in a deep, textured impression that you can feel with your fingertips.</p>
                <p>Our designs draw inspiration from timeless botanical illustrations, classic typography, and the natural beauty of the world around us.</p>
            </div>
        </div>
    </div>
</section>

<section class="section section--sage">
    <div class="container">
        <div class="split-content">
            <div class="split-content__text">
                <h2>Crafted with Intention</h2>
                <p>From the selection of premium cotton paper to the mixing of custom ink colors, every detail is carefully considered. We believe that meaningful moments deserve meaningful paper goods — and that the art of putting pen to paper should be celebrated.</p>
                <p>Whether you're sending a note of sympathy, celebrating a new arrival, or simply saying thank you, Longbourn Papers provides the perfect canvas for your words.</p>
            </div>
            <div class="split-content__image">
                <div style="width:100%;min-height:400px;background:var(--color-rose);display:flex;align-items:center;justify-content:center;">
                    <span style="color:var(--color-text-light);font-family:var(--font-serif);font-size:1.25rem;">Craft Image</span>
                </div>
            </div>
        </div>
    </div>
</section>

<?php
// Display any content from the WordPress editor
while ( have_posts() ) :
    the_post();
    $content = get_the_content();
    if ( ! empty( $content ) ) :
?>
    <section class="section section--cream">
        <div class="container container--narrow">
            <?php the_content(); ?>
        </div>
    </section>
<?php
    endif;
endwhile;
?>

<?php get_footer(); ?>
