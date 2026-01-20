import React from 'react';
import './OceanSkeleton.css';

function OceanSkeleton() {
    return (
        <div className="ocean-skeleton-container">
            {/* Header Skeleton */}
            <div className="skeleton-card sk-header">
                <div className="skeleton-shimmer"></div>
            </div>

            {/* Circular Indicator Skeleton */}
            <div className="sk-circle-box">
                <div className="sk-circle">
                    <div className="skeleton-shimmer"></div>
                </div>
            </div>

            {/* Metrics Grid Skeleton */}
            <div className="sk-grid">
                {[...Array(6)].map((_, i) => (
                    <div key={i} className="skeleton-card sk-card">
                        <div className="skeleton-shimmer"></div>
                    </div>
                ))}
            </div>

            {/* Bottom Actions Skeleton */}
            <div className="skeleton-card sk-card" style={{ marginTop: '20px', height: '60px' }}>
                <div className="skeleton-shimmer"></div>
            </div>
        </div>
    );
}

export default OceanSkeleton;
