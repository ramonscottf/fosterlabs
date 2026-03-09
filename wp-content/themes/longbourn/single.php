<?php
/**
 * Single post template
 *
 * @package Longbourn
 */

get_header();
?>

<article class="single-post">
    <?php if ( has_post_thumbnail() ) : ?>
        <div class="hero" style="min-height:40vh;">
            <div class="hero__image">
                <?php the_post_thumbnail( 'longbourn-hero' ); ?>
            </div>
            <div class="hero__overlay"></div>
            <div class="hero__content">
                <h1 class="hero__title"><?php the_title(); ?></h1>
                <p class="hero__subtitle"><?php echo get_the_date(); ?></p>
            </div>
        </div>
    <?php else : ?>
        <div class="page-header">
            <div class="container">
                <h1><?php the_title(); ?></h1>
                <p><?php echo get_the_date(); ?></p>
            </div>
        </div>
    <?php endif; ?>

    <div class="page-content">
        <div class="container container--narrow">
            <div class="entry-content" style="font-size:1.05rem;line-height:1.9;">
                <?php
                the_content();

                wp_link_pages( array(
                    'before' => '<div class="page-links">' . __( 'Pages:', 'longbourn' ),
                    'after'  => '</div>',
                ) );
                ?>
            </div>

            <div style="margin-top:var(--spacing-xl);padding-top:var(--spacing-md);border-top:1px solid var(--color-border);">
                <?php
                the_post_navigation( array(
                    'prev_text' => '<span style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--color-text-light);">Previous</span><br>%title',
                    'next_text' => '<span style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--color-text-light);">Next</span><br>%title',
                ) );
                ?>
            </div>
        </div>
    </div>
</article>

<?php get_footer(); ?>
