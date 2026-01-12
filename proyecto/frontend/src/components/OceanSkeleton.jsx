import React from 'react';
import './OceanSkeleton.css';

function OceanSkeleton() {
    return (
        <div className="ocean-skeleton-container">
            {/* Header Skeleton */}
            <div className="skeleton-pulse sk-header"></div>

            {/* Circular Indicator Skeleton */}
            <div className="sk-circle-box">
                <div className="skeleton-pulse sk-circle"></div>
            </div>

            {/* Metrics Grid Skeleton */}
            <div className="sk-grid">
                <div className="skeleton-pulse sk-card"></div>
                <div className="skeleton-pulse sk-card"></div>
                <div className="skeleton-pulse sk-card"></div>
                <div className="skeleton-pulse sk-card"></div>
                <div className="skeleton-pulse sk-card"></div>
                <div className="skeleton-pulse sk-card"></div>
            </div>

            {/* Bottom Actions Skeleton */}
            <div className="skeleton-pulse sk-card" style={{ marginTop: '20px', height: '60px' }}></div>
        </div>
    );
}

export default OceanSkeleton;
