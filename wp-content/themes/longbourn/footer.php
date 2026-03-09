<footer class="site-footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <h3>Longbourn Papers</h3>
                <p>Crafted paper goods for meaningful moments. Hand-pressed heirloom stationery created using traditional letterpress techniques on rich cotton paper.</p>
            </div>

            <div class="footer-col">
                <h4>Shop</h4>
                <ul>
                    <li><a href="<?php echo class_exists( 'WooCommerce' ) ? esc_url( wc_get_page_permalink( 'shop' ) ) : '#'; ?>">All Products</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/product-category/gift-tags/' ) ); ?>">Gift Tags</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/product-category/grand-tags/' ) ); ?>">Grand Tags</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/product-category/petite-cards/' ) ); ?>">Petite Cards</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/product-category/stationery/' ) ); ?>">Stationery</a></li>
                </ul>
            </div>

            <div class="footer-col">
                <h4>Collections</h4>
                <ul>
                    <li><a href="<?php echo esc_url( home_url( '/product-category/sympathy/' ) ); ?>">Sympathy & Support</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/product-category/gratitude/' ) ); ?>">Thank You & Gratitude</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/product-category/celebration/' ) ); ?>">Celebration</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/product-category/baby/' ) ); ?>">Baby</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/product-category/holiday/' ) ); ?>">Holiday</a></li>
                </ul>
            </div>

            <div class="footer-col">
                <h4>Connect</h4>
                <ul>
                    <li><a href="<?php echo esc_url( home_url( '/about/' ) ); ?>">About</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/the-art-of-letterpress/' ) ); ?>">Art of Letterpress</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">Contact</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/blog/' ) ); ?>">Blog</a></li>
                    <?php
                    $instagram = get_theme_mod( 'longbourn_social_instagram' );
                    if ( $instagram ) :
                    ?>
                        <li><a href="<?php echo esc_url( $instagram ); ?>" target="_blank" rel="noopener noreferrer">Instagram</a></li>
                    <?php endif; ?>
                </ul>
            </div>
        </div>

        <div class="footer-bottom">
            <p>&copy; <?php echo esc_html( date( 'Y' ) ); ?> Longbourn Papers. All rights reserved.</p>
            <div class="footer-social">
                <?php
                $social_links = array(
                    'instagram' => 'Instagram',
                    'facebook'  => 'Facebook',
                    'pinterest' => 'Pinterest',
                );
                foreach ( $social_links as $key => $label ) :
                    $url = get_theme_mod( "longbourn_social_{$key}" );
                    if ( $url ) :
                ?>
                    <a href="<?php echo esc_url( $url ); ?>" target="_blank" rel="noopener noreferrer"><?php echo esc_html( $label ); ?></a>
                <?php
                    endif;
                endforeach;
                ?>
            </div>
        </div>
    </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
