import { useState, useEffect } from "react";
import styles from "./Component.module.css";

export default function Component() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  return (
    <div className={styles.wrapper}>
      {/* content */}
    </div>
  );
}
