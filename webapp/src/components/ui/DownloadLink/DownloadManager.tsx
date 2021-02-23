/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-static-element-interactions */
import React, { ReactNode, useState, useEffect, ReactText, PropsWithChildren } from 'react';
import { connect, ConnectedProps } from 'react-redux';
import { useSnackbar } from 'notistack';
import { Translation } from 'react-i18next';
import { LinearProgress } from '@material-ui/core';
import { loginUser, logoutAction } from '../../../ducks/auth';
import { refresh } from '../../../services/api/auth';
import { AppState } from '../../../App/reducers';
import { addOnCloseListener, removeOnCloseListener } from '../../../ducks/global';
import { addDownload as addDownloadAction, clearDownload as clearDownloadAction, DownloadItem } from '../../../ducks/download';

const DownloadMessage = (props: {name: string}) => {
  const { name } = props;
  return (
    <div>
      <Translation>{(t) => `${t('studymanager:exporting')}${name}`}</Translation>
      <LinearProgress style={{ width: '100%' }} />
    </div>
  );
};

const mapState = (state: AppState) => ({
  user: state.auth.user,
  downloads: state.download.downloads,
});

const mapDispatch = ({
  login: loginUser,
  logout: logoutAction,
  preventClose: addOnCloseListener,
  clearPreventClose: removeOnCloseListener,
  addDownload: addDownloadAction,
  clearDownload: clearDownloadAction,
});

const connector = connect(mapState, mapDispatch);
type PropsFromRedux = ConnectedProps<typeof connector>;

type PropTypes = PropsFromRedux;

const DownloadManager = (props: PropTypes) => {
  const { user, login, logout, downloads, preventClose, clearPreventClose, clearDownload } = props;
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();
  const [refreshed, setRefreshed] = useState(false);
  const [availableDownloads, setAvailableDownloads] = useState<DownloadItem[]>([]);
  const [preventCloseHandler, setPreventCloseHandler] = useState<string>();
  const [notif, setNotif] = useState<ReactText>();

  const onDownloadAdded = async () => {
    setPreventCloseHandler(preventClose(() => 'Closing will prevent download completion'));
    setRefreshed(false);
    if (user) {
      await refresh(user, login, logout);
    }
    downloads.filter((dl) => availableDownloads.find((adl) => adl.url !== dl.url)).forEach((dl) => {
      setNotif(enqueueSnackbar(<DownloadMessage name={dl.name} />, {
        variant: 'default',
        autoHideDuration: null,
        anchorOrigin: {
          horizontal: 'right',
          vertical: 'bottom',
        },
      }));
    });
    setAvailableDownloads(downloads);

    // eslint-disable-next-line no-restricted-globals
    // location.href = url;
    setRefreshed(true);
  };

  useEffect(() => {
    onDownloadAdded();
  }, [downloads]);

  useEffect(() => {
    if (preventCloseHandler) {
      clearPreventClose(preventCloseHandler);
    }
  }, []);

  const loaded = (id: string) => {
    if (notif) {
      closeSnackbar(notif);
    }
    if (preventCloseHandler) {
      clearPreventClose(preventCloseHandler);
    }
    setTimeout(() => {
      //clearDownload(id);
    }, 1000);
  };

  return (
    <>
      <div style={{ display: 'none' }}>
        {refreshed && availableDownloads.map((dl) => (
          <iframe width="0" height="0" title={dl.url} id={dl.url} key={dl.url} src={dl.url} onLoad={() => loaded(dl.url)} />
        ))}
      </div>
    </>
  );
};

export default connector(DownloadManager);
