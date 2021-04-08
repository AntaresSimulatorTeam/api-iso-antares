import React, { useState, useEffect } from 'react';
import { connect, ConnectedProps } from 'react-redux';
import debug from 'debug';
import { useTranslation } from 'react-i18next';
import { createStyles, makeStyles, Theme } from '@material-ui/core';
import { useSnackbar } from 'notistack';
import { AppState } from '../reducers';
import { logoutAction } from '../../ducks/auth';
import { getUsers, UserDTO } from '../../services/api/user';
import UserInfo from '../../components/UserInfo';

// pour logger des jolis logs (filtrable en conf)
const logError = debug('antares:loginpanel:error');

// mécanique de style Material-UI (parfois pas utilisé et je fais directement <div style={{...}} /> pour aller plus vite.. ^^')
// est utilisé dans le composant (commentaire ensuite)
const useStyles = makeStyles((theme: Theme) => createStyles({
  root: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
  },
}));

// pour connecter à redux les 3 choses suivantes et wrapper le composant à l'export (derniere ligne)
const mapState = (state: AppState) => ({
  user: state.auth.user,
});

const mapDispatch = ({
  logout: logoutAction,
});

const connector = connect(mapState, mapDispatch);

// Quand le composant et wrappé le type des props est défini comme ceci
type ReduxProps = ConnectedProps<typeof connector>;
type PropTypes = ReduxProps;

const AdminPanel = (props: PropTypes) => {
  // Déconstruction de l'objet props en variables simple
  const { user, logout } = props;
  // pour récupérer l'objet contenant le nom des classes css générées par Material UI
  const classes = useStyles();
  // utilisé un peu partout pour toutes les string qui doivent être affichées (et traduites)
  // s'utilise comme ça : t('namespace:text_key')
  // cela retourne la string traduite en utilisant le fichier public/locales/{lang}/namespace et la clé text_key
  // attention si on veut rajouter un fichier de trad, il faut le spécifier dans i18n.js (à la racine)
  const [t] = useTranslation();
  // lib https://iamhosseindhv.com/notistack qui permet d'afficher simplement des notifs material ui
  const { enqueueSnackbar } = useSnackbar();
  // une modification du state (via setAuthorized pour cette variable) trigger un rerender lorsque la variable à changer
  // attention (pareil pour le state redux) à bien remplacer la variable et non pas la muter (car le check se fait sur la référence)
  // par exemple si le state était un objet, ce qui suit ne trigger pas de changement :
  // const [myVar, setMyVar] = useState({foo: 'bar'});
  // myVar.foo = 'baz'
  // setMyVar(myVar) // => pas de rerender
  const [authorized, setAuthorized] = useState(false);
  const [userList, setUserList] = useState<UserDTO[]>([]);

  const init = async () => {
    // par exemple vérifier si l'utilisateur est bien admin et faire un setAuthorized(true)
    // on peut utiliser jwt_decode(user.accessToken) pour accéder au propriété du jwt
    setAuthorized(true);

    // par exemple ici on récupere la liste des utilisateurs (à noter que la méthode est "async" ce qui permet d'utiliser await)
    try {
      const users = await getUsers();
      // on met à jour le state
      setUserList(users);
    } catch (e) {
      // au cas ou l'appel fail cela affiche une notif
      enqueueSnackbar(t('main:unknown'), { variant: 'error' });
    }
  };

  // s'execute quand le user change
  useEffect(() => {
    init();
  }, [user]);

  return (
    // recupération et application de nom de class css avec className=...
    // ici selon la valeur du state "authorized" affiche des choses différentes
    // il y a un mapping de la liste des user vers un composant
    <div className={classes.root}>
      {authorized && (
        <div>
          <div>admin panel</div>
          <div>
            {userList.map((u) => <UserInfo user={u} />)}
          </div>
        </div>
      )}
      {!authorized && <div>unauthorized!</div>}
    </div>
  );
};

// on pourrait ensuite wrapper AdminPanel dans un autre composant générique qui vérifie les permissions
// genre un <Protected role={[WRTIER]} admin={false}><ComponentThatNeedProtection ... /></Protected>
export default connector(AdminPanel);
