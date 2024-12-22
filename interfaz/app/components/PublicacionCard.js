import styles from "./PublicacionCard.module.css";
import { FaFileDownload } from "react-icons/fa";

export default function PublicacionCard(props) {
  const { x, color } = props;

  const downloadFile = async (fileId, fileName) => { // NUEVO
    // pasar id y nombre del archivo a la ruta de descarga
    window.location.href = `http://172.233.25.94:5000/archivo/${fileId}/${fileName}`;
    console.log(window.location.href)
  };

  return (
    <div
      className={styles.divPublicacion}
      style={{ borderColor: color }}
    >
      <div
        className={styles.divPublicacionHeader}
        style={{ backgroundColor: color }}
      >
        <p className={styles.divPublicacionTitle}>{x.titulo}</p>
        <p className={styles.divPublicacionAuthor}>Usuario: {x.publicador}</p>
        <p className={styles.divPublicacionDate}>Fecha: {x.fecha_publicacion}</p>
      </div>

      <div className={styles.divPublicacionFiles}>
        <p className={styles.divPublicacionDescription}>
          Descripción: {x.descripcion}
        </p>
        <div
          className={styles.divFilesList}
          style={{ overflowX: x.archivos.length >= 3 ? "scroll" : "hidden" }}
        >
          {x.archivos.map((y, index) => (
            <div
              className={styles.divFile}
              key={index}
              style={{ hover: { backgroundColor: color } }}
              onClick={() => downloadFile(y.id_drive, y.name)}
            >
              <FaFileDownload />
              <p className={styles.divFileName}>{y.name}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
