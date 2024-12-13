import styles from "./PublicacionCard.module.css";
import { FaFileDownload } from "react-icons/fa";

export default function PublicacionCard(props) {
  const { x, color } = props;
  return (
    <div
      className={styles.divPublicacion}
      style={{ borderColor: color }}
    >
      <div
        className={styles.divPublicacionHeader}
        style={{ backgroundColor: color }}
      >
        <p className={styles.divPublicacionTitle}>{x.nombre}</p>
        <p className={styles.divPublicacionAuthor}>Usuario: {x.publicador}</p>
        <p className={styles.divPublicacionDate}>Fecha: {x.fecha}</p>
      </div>

      <div className={styles.divPublicacionFiles}>
        <p className={styles.divPublicacionDescription}>
          Descripción: {x.descripcion}
        </p>
        <div
          className={styles.divFilesList}
          style={{ overflowX: x.archivos.length > 4 ? "scroll" : "hidden" }}
        >
          {x.archivos.map((y, index) => (
            <div
              className={styles.divFile}
              key={index}
              style={{ hover: { backgroundColor: color } }}
            >
              <FaFileDownload />
              <p className={styles.divFileName}>{y.nombre}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
