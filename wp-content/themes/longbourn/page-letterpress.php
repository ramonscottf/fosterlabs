<?php
/**
 * Template Name: Art of Letterpress
 * The Art of Letterpress page template
 *
 * @package Longbourn
 */

get_header();
?>

<section class="hero" style="min-height:50vh;">
    <?php if ( has_post_thumbnail() ) : ?>
        <div class="hero__image">
            <?php the_post_thumbnail( 'longbourn-hero' ); ?>
        </div>
        <div class="hero__overlay"></div>
    <?php else : ?>
        <div style="position:absolute;inset:0;background:var(--color-forest);"></div>
    <?php endif; ?>
    <div class="hero__content">
        <h1 class="hero__title">The Art of Letterpress</h1>
        <p class="hero__subtitle">A centuries-old craft, reimagined for modern correspondence</p>
    </div>
</section>

<section class="section section--cream">
    <div class="container">
        <div class="about-intro">
            <h2>A Time-Honored Tradition</h2>
            <p>Letterpress printing dates back to the 15th century when Johannes Gutenberg invented movable type. Today, we honor this tradition by using antique presses and hand-set type to create stationery with a depth and character that digital printing simply cannot replicate.</p>
        </div>
    </div>
</section>

<section class="section section--sage">
    <div class="container">
        <div class="split-content">
            <div class="split-content__image">
                <div style="width:100%;min-height:400px;background:var(--color-cream-dark);display:flex;align-items:center;justify-content:center;">
                    <span style="color:var(--color-text-light);font-family:var(--font-serif);font-size:1.25rem;">Press Image</span>
                </div>
            </div>
            <div class="split-content__text">
                <h2>The Process</h2>
                <p>Each design begins as a hand-drawn illustration or carefully composed typographic layout. The design is then transferred to a photopolymer plate, which is locked into our antique press.</p>
                <p>Rich, custom-mixed inks are rolled onto the plate, and each sheet of cotton paper is fed through the press by hand. The result is a deeply impressed print with a tactile quality that is instantly recognizable.</p>
            </div>
        </div>
    </div>
</section>

<section class="section section--cream">
    <div class="container">
        <div class="split-content">
            <div class="split-content__text">
                <h2>Our Materials</h2>
                <p>We exclusively use premium cotton paper — a material that is naturally soft, durable, and perfectly suited to the letterpress process. Cotton paper accepts ink beautifully and creates a pronounced impression that sets our stationery apart.</p>
                <p>Our satin ribbons, envelopes, and packaging are all chosen to complement the quality and elegance of the printed pieces they accompany.</p>
            </div>
            <div class="split-content__image">
                <div style="width:100%;min-height:400px;background:var(--color-rose);display:flex;align-items:center;justify-content:center;">
                    <span style="color:var(--color-text-light);font-family:var(--font-serif);font-size:1.25rem;">Materials Image</span>
                </div>
            </div>
        </div>
    </div>
</section>

<?php
while ( have_posts() ) :
    the_post();
    $content = get_the_content();
    if ( ! empty( $content ) ) :
?>
    <section class="section section--sage">
        <div class="container container--narrow">
            <?php the_content(); ?>
        </div>
    </section>
<?php
    endif;
endwhile;
?>

<?php get_footer(); ?>
