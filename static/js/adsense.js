/**
 * Google AdSense Management for Răsfățul Pescarului
 * Handles ad loading, GDPR compliance, and performance optimization
 */

(function() {
    'use strict';

    // AdSense Configuration
    const ADSENSE_CONFIG = {
        client: 'ca-pub-4988585637197167',
        enableLazyLoading: true,
        enableGDPRCompliance: true,
        retryAttempts: 3,
        retryDelay: 2000
    };

    // AdSense Manager Class
    class AdSenseManager {
        constructor() {
            this.adsLoaded = false;
            this.consentGiven = false;
            this.retryCount = 0;
            this.init();
        }

        init() {
            // Check for cookie consent
            this.checkConsent();
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Initialize ads if consent is given
            if (this.consentGiven) {
                this.loadAds();
            }
        }

        checkConsent() {
            // Check if cookies are accepted
            this.consentGiven = document.body.classList.contains('cookies-accepted');
            
            // Also check cookieconsent library if available
            if (window.cookieconsent && window.cookieconsent.hasConsented) {
                this.consentGiven = window.cookieconsent.hasConsented();
            }
        }

        setupEventListeners() {
            // Listen for consent changes
            document.addEventListener('cookieConsentChanged', () => {
                this.checkConsent();
                if (this.consentGiven && !this.adsLoaded) {
                    this.loadAds();
                }
            });

            // Listen for page visibility changes to optimize ad loading
            document.addEventListener('visibilitychange', () => {
                if (!document.hidden && this.consentGiven && !this.adsLoaded) {
                    this.loadAds();
                }
            });
        }

        loadAds() {
            if (!this.consentGiven || this.adsLoaded) {
                return;
            }

            try {
                // Initialize AdSense
                if (typeof adsbygoogle !== 'undefined') {
                    // Push all ad units
                    const adUnits = document.querySelectorAll('.adsbygoogle');
                    adUnits.forEach(ad => {
                        if (!ad.dataset.adsbygoogleStatus) {
                            (adsbygoogle = window.adsbygoogle || []).push({});
                        }
                    });
                    
                    this.adsLoaded = true;
                    this.retryCount = 0;
                    
                    // Add success class to body
                    document.body.classList.add('ads-loaded');
                    
                    console.log('AdSense ads loaded successfully');
                } else {
                    throw new Error('AdSense script not loaded');
                }
            } catch (error) {
                console.warn('Failed to load AdSense ads:', error);
                this.retryLoadAds();
            }
        }

        retryLoadAds() {
            if (this.retryCount < ADSENSE_CONFIG.retryAttempts) {
                this.retryCount++;
                console.log(`Retrying AdSense load (attempt ${this.retryCount})`);
                
                setTimeout(() => {
                    this.loadAds();
                }, ADSENSE_CONFIG.retryDelay * this.retryCount);
            } else {
                console.error('Failed to load AdSense after maximum retry attempts');
                this.handleAdLoadFailure();
            }
        }

        handleAdLoadFailure() {
            // Hide ad containers if ads fail to load
            const adContainers = document.querySelectorAll('.ad-container, .ad-banner, .ad-sidebar, .ad-inline');
            adContainers.forEach(container => {
                container.style.display = 'none';
            });
            
            document.body.classList.add('ads-failed');
        }

        // Method to manually refresh ads (useful for SPA navigation)
        refreshAds() {
            if (!this.consentGiven) {
                return;
            }

            try {
                const adUnits = document.querySelectorAll('.adsbygoogle');
                adUnits.forEach(ad => {
                    if (ad.dataset.adsbygoogleStatus === 'done') {
                        // Clear the ad
                        ad.innerHTML = '';
                        ad.removeAttribute('data-adsbygoogle-status');
                        
                        // Reload the ad
                        (adsbygoogle = window.adsbygoogle || []).push({});
                    }
                });
            } catch (error) {
                console.warn('Failed to refresh ads:', error);
            }
        }

        // Method to handle lazy loading of ads
        setupLazyLoading() {
            if (!ADSENSE_CONFIG.enableLazyLoading) {
                return;
            }

            const adContainers = document.querySelectorAll('.ad-container, .ad-banner, .ad-sidebar, .ad-inline');
            
            if ('IntersectionObserver' in window) {
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const adUnit = entry.target.querySelector('.adsbygoogle');
                            if (adUnit && !adUnit.dataset.adsbygoogleStatus && this.consentGiven) {
                                (adsbygoogle = window.adsbygoogle || []).push({});
                            }
                            observer.unobserve(entry.target);
                        }
                    });
                }, {
                    rootMargin: '100px'
                });

                adContainers.forEach(container => {
                    observer.observe(container);
                });
            }
        }

        // Method to track ad performance
        trackAdPerformance() {
            // Basic ad performance tracking
            const adUnits = document.querySelectorAll('.adsbygoogle');
            let loadedAds = 0;
            let failedAds = 0;

            adUnits.forEach(ad => {
                if (ad.dataset.adsbygoogleStatus === 'done') {
                    loadedAds++;
                } else if (ad.dataset.adsbygoogleStatus === 'error') {
                    failedAds++;
                }
            });

            // Log performance metrics
            console.log(`Ad Performance: ${loadedAds} loaded, ${failedAds} failed`);
            
            // You can send this data to your analytics service
            if (window.gtag) {
                gtag('event', 'ad_performance', {
                    'loaded_ads': loadedAds,
                    'failed_ads': failedAds,
                    'total_ads': adUnits.length
                });
            }
        }
    }

    // Utility functions
    const AdSenseUtils = {
        // Check if ad blocker is present
        isAdBlockerActive() {
            const testAd = document.createElement('div');
            testAd.innerHTML = '&nbsp;';
            testAd.className = 'adsbox';
            testAd.style.position = 'absolute';
            testAd.style.left = '-10000px';
            document.body.appendChild(testAd);
            
            const isBlocked = testAd.offsetHeight === 0;
            document.body.removeChild(testAd);
            
            return isBlocked;
        },

        // Get optimal ad sizes based on viewport
        getOptimalAdSize() {
            const width = window.innerWidth;
            
            if (width < 768) {
                return { width: 320, height: 50 }; // Mobile banner
            } else if (width < 1024) {
                return { width: 728, height: 90 }; // Tablet leaderboard
            } else {
                return { width: 970, height: 250 }; // Desktop large banner
            }
        },

        // Handle responsive ad sizing
        handleResponsiveAds() {
            const responsiveAds = document.querySelectorAll('.adsbygoogle[data-full-width-responsive="true"]');
            
            responsiveAds.forEach(ad => {
                const container = ad.closest('.ad-container, .ad-banner, .ad-sidebar, .ad-inline');
                if (container) {
                    const containerWidth = container.offsetWidth;
                    ad.style.maxWidth = containerWidth + 'px';
                }
            });
        }
    };

    // Initialize AdSense Manager when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        // Check for ad blocker
        if (AdSenseUtils.isAdBlockerActive()) {
            console.warn('Ad blocker detected');
            document.body.classList.add('adblocker-detected');
        }

        // Initialize AdSense Manager
        window.adSenseManager = new AdSenseManager();
        
        // Set up lazy loading
        window.adSenseManager.setupLazyLoading();
        
        // Handle responsive ads on resize
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                AdSenseUtils.handleResponsiveAds();
            }, 250);
        });
        
        // Track ad performance after page load
        window.addEventListener('load', () => {
            setTimeout(() => {
                window.adSenseManager.trackAdPerformance();
            }, 5000);
        });
    });

    // Export utilities for global access
    window.AdSenseUtils = AdSenseUtils;

})();
