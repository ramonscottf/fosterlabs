<?php
/**
 * Template Name: Front Page
 * Homepage template for Longbourn Papers
 *
 * @package Longbourn
 */

get_header();

$hero_title    = get_theme_mod( 'longbourn_hero_title', 'Elevate Every Gift' );
$hero_subtitle = get_theme_mod( 'longbourn_hero_subtitle', 'Hand-pressed heirloom stationery crafted with traditional techniques on rich cotton paper.' );
$hero_cta_text = get_theme_mod( 'longbourn_hero_cta_text', 'Shop Tags' );
$hero_cta_url  = get_theme_mod( 'longbourn_hero_cta_url', '/shop' );
$hero_image_id = get_theme_mod( 'longbourn_hero_image' );
$hero_image    = $hero_image_id ? wp_get_attachment_image_url( $hero_image_id, 'longbourn-hero' ) : '';
?>

<!-- Hero Section -->
<section class="hero">
    <?php if ( $hero_image ) : ?>
        <div class="hero__image">
            <img src="<?php echo esc_url( $hero_image ); ?>" alt="<?php echo esc_attr( $hero_title ); ?>">
        </div>
        <div class="hero__overlay"></div>
    <?php endif; ?>
    <div class="hero__content">
        <h1 class="hero__title"><?php echo esc_html( $hero_title ); ?></h1>
        <p class="hero__subtitle"><?php echo esc_html( $hero_subtitle ); ?></p>
        <a href="<?php echo esc_url( $hero_cta_url ); ?>" class="btn btn--outline"><?php echo esc_html( $hero_cta_text ); ?></a>
    </div>
</section>

<!-- Featured Products -->
<?php if ( class_exists( 'WooCommerce' ) ) : ?>
<section class="section section--cream">
    <div class="container">
        <div class="featured-text">
            <h2>Our Favorites</h2>
            <p>Timeless designs, hand-pressed with care on luxurious cotton paper.</p>
        </div>
        <div class="products-grid">
            <?php
            $args = array(
                'post_type'      => 'product',
                'posts_per_page' => 4,
                'meta_key'       => '_featured',
                'meta_value'     => 'yes',
                'orderby'        => 'date',
                'order'          => 'DESC',
            );

            // Fallback to recent products if no featured products
            $featured = new WP_Query( $args );
            if ( ! $featured->have_posts() ) {
                $args = array(
                    'post_type'      => 'product',
                    'posts_per_page' => 4,
                    'orderby'        => 'date',
                    'order'          => 'DESC',
                );
                $featured = new WP_Query( $args );
            }

            while ( $featured->have_posts() ) :
                $featured->the_post();
                global $product;
            ?>
                <div class="product-card">
                    <a href="<?php the_permalink(); ?>">
                        <div class="product-card__image">
                            <?php if ( has_post_thumbnail() ) : ?>
                                <?php the_post_thumbnail( 'longbourn-product' ); ?>
                            <?php else : ?>
                                <div style="width:100%;height:100%;background:var(--color-cream-dark);display:flex;align-items:center;justify-content:center;color:var(--color-text-light);">No Image</div>
                            <?php endif; ?>
                        </div>
                        <div class="product-card__info">
                            <h3 class="product-card__title"><?php the_title(); ?></h3>
                            <div class="product-card__price"><?php echo $product->get_price_html(); ?></div>
                        </div>
                    </a>
                </div>
            <?php
            endwhile;
            wp_reset_postdata();
            ?>
        </div>
        <div style="text-align:center;margin-top:var(--spacing-lg);">
            <a href="<?php echo esc_url( wc_get_page_permalink( 'shop' ) ); ?>" class="btn btn--outline-dark">View All Products</a>
        </div>
    </div>
</section>
<?php endif; ?>

<!-- Brand Story Section -->
<section class="section section--sage">
    <div class="container">
        <div class="split-content">
            <div class="split-content__image">
                <?php
                $story_image_id = get_theme_mod( 'longbourn_story_image' );
                if ( $story_image_id ) :
                    echo wp_get_attachment_image( $story_image_id, 'large' );
                else :
                ?>
                    <div style="width:100%;min-height:400px;background:var(--color-rose);display:flex;align-items:center;justify-content:center;">
                        <span style="color:var(--color-text-light);font-family:var(--font-serif);font-size:1.25rem;">Brand Image</span>
                    </div>
                <?php endif; ?>
            </div>
            <div class="split-content__text">
                <h2>Crafted Paper Goods for Meaningful Moments</h2>
                <p>Every piece from Longbourn Papers is hand-pressed using traditional letterpress techniques, creating a tactile impression on luxurious cotton paper. Our heirloom-quality stationery brings intention and beauty to your most meaningful exchanges.</p>
                <a href="<?php echo esc_url( home_url( '/about/' ) ); ?>" class="btn btn--outline-dark">Our Story</a>
            </div>
        </div>
    </div>
</section>

<!-- Collections -->
<section class="section section--cream">
    <div class="container">
        <div class="featured-text">
            <h2>Shop by Collection</h2>
            <p>Find the perfect sentiment for every occasion.</p>
        </div>
        <?php if ( class_exists( 'WooCommerce' ) ) : ?>
            <div class="collections-grid">
                <?php
                $collections = get_terms( array(
                    'taxonomy'   => 'product_cat',
                    'hide_empty' => false,
                    'number'     => 6,
                    'orderby'    => 'name',
                ) );

                if ( ! empty( $collections ) && ! is_wp_error( $collections ) ) :
                    foreach ( $collections as $collection ) :
                        $thumbnail_id = get_term_meta( $collection->term_id, 'thumbnail_id', true );
                ?>
                    <a href="<?php echo esc_url( get_term_link( $collection ) ); ?>" class="collection-card">
                        <?php if ( $thumbnail_id ) : ?>
                            <?php echo wp_get_attachment_image( $thumbnail_id, 'longbourn-collection' ); ?>
                        <?php else : ?>
                            <div style="position:absolute;inset:0;background:var(--color-forest-light);"></div>
                        <?php endif; ?>
                        <div class="collection-card__overlay">
                            <h3 class="collection-card__title"><?php echo esc_html( $collection->name ); ?></h3>
                        </div>
                    </a>
                <?php
                    endforeach;
                endif;
                ?>
            </div>
        <?php else : ?>
            <div class="collections-grid">
                <?php
                $placeholder_collections = array(
                    'Sympathy & Support',
                    'Thank You & Gratitude',
                    'Celebration',
                    'Baby',
                    'Holiday',
                    'Our Papers & Provisions',
                );
                foreach ( $placeholder_collections as $name ) :
                ?>
                    <div class="collection-card">
                        <div style="position:absolute;inset:0;background:var(--color-forest-light);"></div>
                        <div class="collection-card__overlay">
                            <h3 class="collection-card__title"><?php echo esc_html( $name ); ?></h3>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </div>
</section>

<!-- Letterpress Section -->
<section class="section section--forest">
    <div class="container">
        <div class="split-content">
            <div class="split-content__text">
                <h2>The Art of Letterpress</h2>
                <p>Each design is carefully composed using traditional techniques that date back centuries. The result is a tactile, deeply impressed print that you can feel with your fingertips — a quality that simply cannot be replicated by modern printing methods.</p>
                <a href="<?php echo esc_url( home_url( '/the-art-of-letterpress/' ) ); ?>" class="btn btn--outline">Learn More</a>
            </div>
            <div class="split-content__image">
                <?php
                $letterpress_image_id = get_theme_mod( 'longbourn_letterpress_image' );
                if ( $letterpress_image_id ) :
                    echo wp_get_attachment_image( $letterpress_image_id, 'large' );
                else :
                ?>
                    <div style="width:100%;min-height:400px;background:var(--color-forest-light);display:flex;align-items:center;justify-content:center;">
                        <span style="color:var(--color-cream);font-family:var(--font-serif);font-size:1.25rem;">Letterpress Image</span>
                    </div>
                <?php endif; ?>
            </div>
        </div>
    </div>
</section>

<!-- Newsletter -->
<section class="section section--rose">
    <div class="container">
        <div class="newsletter">
            <h2>Stay in Touch</h2>
            <p>Join our mailing list for new designs, seasonal collections, and the occasional love letter.</p>
            <form class="newsletter-form" action="#" method="post">
                <input type="email" name="newsletter_email" placeholder="Your email address" required>
                <button type="submit">Subscribe</button>
            </form>
        </div>
    </div>
</section>

<?php get_footer(); ?>
