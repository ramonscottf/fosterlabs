<?php
/**
 * Template Name: Contact Page
 * Contact page template for Longbourn Papers
 *
 * @package Longbourn
 */

get_header();

$phone   = get_theme_mod( 'longbourn_phone', '801-205-6642' );
$email   = get_theme_mod( 'longbourn_email', 'alexandra@longbournpapers.com' );
$address = get_theme_mod( 'longbourn_address', 'PO Box 22, Farmington UT 84025' );
?>

<!-- Hero -->
<section class="section section--sage">
    <div class="container">
        <div class="split-content">
            <div class="split-content__image">
                <?php if ( has_post_thumbnail() ) : ?>
                    <?php the_post_thumbnail( 'large' ); ?>
                <?php else : ?>
                    <div style="width:100%;min-height:400px;background:var(--color-rose);display:flex;align-items:center;justify-content:center;">
                        <span style="color:var(--color-text-light);font-family:var(--font-serif);font-size:1.25rem;">Contact Image</span>
                    </div>
                <?php endif; ?>
            </div>
            <div class="split-content__text">
                <h1>Get in Touch</h1>
                <p>At Longbourn, we adore the romance of a handwritten letter sealed with wax and posted in a bright red box. But we understand that modern communication methods are a bit more convenient for shopping. Please feel free to reach out through any channel you prefer.</p>

                <div style="margin-top:var(--spacing-md);">
                    <p><strong>Phone:</strong> <a href="tel:<?php echo esc_attr( str_replace( '-', '', $phone ) ); ?>"><?php echo esc_html( $phone ); ?></a></p>
                    <p><strong>Email:</strong> <a href="mailto:<?php echo esc_attr( $email ); ?>"><?php echo esc_html( $email ); ?></a></p>
                    <p><strong>Mail:</strong> <?php echo esc_html( $address ); ?></p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Contact Form -->
<section class="section section--cream">
    <div class="container">
        <div class="featured-text">
            <h2>Write to Us</h2>
        </div>

        <div class="contact-form">
            <form method="post" action="">
                <?php wp_nonce_field( 'longbourn_contact', 'longbourn_contact_nonce' ); ?>

                <div class="form-group">
                    <label for="contact_name">Name *</label>
                    <input type="text" id="contact_name" name="contact_name" required>
                </div>

                <div class="form-group">
                    <label for="contact_email">Email *</label>
                    <input type="email" id="contact_email" name="contact_email" required>
                </div>

                <div class="form-group">
                    <label for="contact_phone">Phone</label>
                    <input type="tel" id="contact_phone" name="contact_phone">
                </div>

                <div class="form-group">
                    <label for="contact_type">Inquiry Type</label>
                    <select id="contact_type" name="contact_type">
                        <option value="">Select an option</option>
                        <option value="General Inquiry">General Inquiry</option>
                        <option value="Wholesale">Wholesale</option>
                        <option value="Custom Orders">Custom Orders</option>
                        <option value="Order Support">Order Support</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="contact_message">Comment *</label>
                    <textarea id="contact_message" name="contact_message" required></textarea>
                </div>

                <button type="submit" class="btn btn--primary" style="width:100%;">Send</button>
            </form>
        </div>
    </div>
</section>

<!-- Before You Go -->
<?php if ( class_exists( 'WooCommerce' ) ) : ?>
<section class="section section--rose">
    <div class="container">
        <div class="featured-text">
            <h2>Before You Go&hellip;</h2>
            <p>Browse our collection of handcrafted gift tags, perfect for elevating every gift.</p>
            <a href="<?php echo esc_url( home_url( '/product-category/gift-tags/' ) ); ?>" class="btn btn--outline-dark" style="margin-top:var(--spacing-sm);">Shop Gift Tags</a>
        </div>
    </div>
</section>
<?php endif; ?>

<?php get_footer(); ?>
