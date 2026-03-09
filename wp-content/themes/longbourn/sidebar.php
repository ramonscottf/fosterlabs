<?php
/**
 * Sidebar template
 *
 * @package Longbourn
 */

if ( ! is_active_sidebar( 'shop-sidebar' ) ) {
    return;
}
?>

<aside class="widget-area" role="complementary">
    <?php dynamic_sidebar( 'shop-sidebar' ); ?>
</aside>
