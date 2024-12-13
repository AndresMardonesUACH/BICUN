import styles from "./AsignaturaCard.module.css"


export default function AsignaturaCard(props) {
    const {nombre, prefijo, codigo, color} = props
    return (
        <div className={styles.divAsignatura} style={{borderColor: color}}>
            <div className={styles.divAsignatura_info}>
                <p className={styles.asignaturaTitle}>{nombre}</p>
                <p className={styles.asignaturaTitle}>{prefijo}-{codigo}</p>
            </div>
            <div className={styles.divAsignatura_block} style={{backgroundColor: color}}></div>
        </div>
    )
}