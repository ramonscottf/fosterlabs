<?php
/**
 * Search results template
 *
 * @package Longbourn
 */

get_header();
?>

<div class="page-header">
    <div class="container">
        <h1><?php printf( esc_html__( 'Search Results for: %s', 'longbourn' ), get_search_query() ); ?></h1>
    </div>
</div>

<div class="page-content">
    <div class="container">
        <?php if ( have_posts() ) : ?>
            <div class="blog-grid">
                <?php while ( have_posts() ) : the_post(); ?>
                    <article class="blog-card">
                        <?php if ( has_post_thumbnail() ) : ?>
                            <a href="<?php the_permalink(); ?>" class="blog-card__image">
                                <?php the_post_thumbnail( 'longbourn-blog' ); ?>
                            </a>
                        <?php endif; ?>
                        <div class="blog-card__content">
                            <div class="blog-card__date"><?php echo get_the_date(); ?></div>
                            <h2 class="blog-card__title">
                                <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                            </h2>
                            <div class="blog-card__excerpt"><?php the_excerpt(); ?></div>
                        </div>
                    </article>
                <?php endwhile; ?>
            </div>

            <div style="text-align:center;margin-top:var(--spacing-lg);">
                <?php
                the_posts_pagination( array(
                    'mid_size'  => 2,
                    'prev_text' => '&laquo; Previous',
                    'next_text' => 'Next &raquo;',
                ) );
                ?>
            </div>
        <?php else : ?>
            <div class="featured-text">
                <h2>No Results Found</h2>
                <p>Sorry, nothing matched your search. Please try a different term.</p>
                <div style="max-width:400px;margin:var(--spacing-md) auto 0;">
                    <?php get_search_form(); ?>
                </div>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php get_footer(); ?>
