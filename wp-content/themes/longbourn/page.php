<?php
/**
 * Default page template
 *
 * @package Longbourn
 */

get_header();
?>

<div class="page-header">
    <div class="container">
        <h1><?php the_title(); ?></h1>
    </div>
</div>

<div class="page-content">
    <div class="container container--narrow">
        <?php
        while ( have_posts() ) :
            the_post();
            the_content();
        endwhile;
        ?>
    </div>
</div>

<?php get_footer(); ?>
