"use client";

import React, { useEffect, useRef, useState } from "react";

import "leaflet/dist/leaflet.css";

//@ts-expect-error trust me bro
import { MaptilerLayer } from "@maptiler/leaflet-maptilersdk";
import L from "leaflet";

import PinBlack from "../../../../public/pin_black.png";
import styles from "./map.module.css";

const Pin = new L.Icon({
    iconUrl: PinBlack.src,
    iconSize: [32, 32], // size of the icon
    iconAnchor: [16, 32], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -32], // point from which the popup should open relative to the iconAnchor
});

const Map = () => {
    const mapContainer = useRef(null);
    const map = useRef(null);
    const center = { lng: -122.272507, lat: 37.866989 };
    const [zoom] = useState(17);

    useEffect(() => {
        if (map.current) return; // stops map from intializing more than once

        //@ts-expect-error trust me bro
        map.current = new L.Map(mapContainer.current, {
            center: L.latLng(center.lat, center.lng),
            zoom: zoom,
            dragging: false,
            scrollWheelZoom: false,
            doubleClickZoom: false,
            touchZoom: false,
            boxZoom: false,
            keyboard: false,
        });

        // Create a MapTiler Layer inside Leaflet
        const mtLayer = new MaptilerLayer({
            // Get your free API key at https://cloud.maptiler.com
            apiKey: process.env.NEXT_PUBLIC_MAPTILER_API_KEY,
        });

        mtLayer.addTo(map.current);

        const marker1 = L.marker([37.867989, -122.271507], { icon: Pin }); // King Center

        const marker2 = L.marker([33.634023, -117.851286], { icon: Pin });
        const marker3 = L.marker([33.634917, -117.862744], { icon: Pin });

        marker1
            .addTo(map.current!)
            .bindPopup("<b>Richard Davis</b><br>ID: #272428");
        marker2
            .addTo(map.current!)
            .bindPopup("<b>Sophia Jones</b><br>ID: #121445");
        marker3
            .addTo(map.current!)
            .bindPopup("<b>Adam Smith</b><br>ID: #920232");
    }, [center.lng, center.lat, zoom]);

    return (
        <div className={styles.mapWrap}>
            <div ref={mapContainer} className={styles.map} />
        </div>
    );
};

export default Map;
